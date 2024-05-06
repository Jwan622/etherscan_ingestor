import requests
import typer
import threading
import re
import time
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor

from src.assignment.config import CONFIG, RECORD_RETRIEVAL_LIMIT, API_KEY, THREADS_COUNT, SEMAPHOR_THREADS_COUNT, \
    DEFAULT_ADDRESS, DEV_MODE, DEV_MODE_ENDING_MULTIPLE, API_RATE_LIMIT_DELAY, BASE_BLOCK_ATTEMPT, BLOCK_ATTEMPTS
from src.assignment.db import init_db
from src.assignment.logger import logger
from src.assignment.models import Address, Transaction
from src.assignment.config import DATABASE_URI


app = typer.Typer()

api_call_semaphore = threading.Semaphore(SEMAPHOR_THREADS_COUNT)
Session = init_db(DATABASE_URI)


def __log_thread_error(thread_id, current_block, ending_block):
    error_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"Error at {error_time}, Thread ID: {thread_id}, Current Block: {current_block}, Ending Block: {ending_block}"
    logger.error(log_msg)


def __log_with_thread_id(message, thread_id):
    full_message = f"thread_id: {thread_id}. Message: {message}"
    logger.info(full_message)


def __call_etherscan(address, thread_id=None, startblock=0, endblock=99999999, sort="asc", retries=6,
                     delay=API_RATE_LIMIT_DELAY):
    api_url = (
        "https://api.etherscan.io/api?module=account&action=txlistinternal&"
        f"address={address}&startblock={startblock}&endblock={endblock}&"
        f"page=1&offset={RECORD_RETRIEVAL_LIMIT}&sort={sort}&apikey={API_KEY}"
    )

    for attempt in range(retries):
        with api_call_semaphore:
            __log_with_thread_id(
                f"Calling Etherscan API with current_block: {startblock}, ending_block: {endblock}, thread_id: {thread_id}",
                thread_id)
            response = requests.get(api_url)
            data = response.json()
            time.sleep(delay)

        if data['result'] != 'Max rate limit reached':
            return data

    __log_thread_error(thread_id, startblock, endblock)
    raise Exception("Max rate limit reached after retrying")


def __get_or_create_address(session, address):
    try:
        addr_obj = session.query(Address).filter_by(address=address).one_or_none()
        if not addr_obj:
            addr_obj = Address(address=address)
            session.add(addr_obj)
            session.commit()

        return addr_obj.id
    except IntegrityError:
        session.rollback()
        addr_obj = session.query(Address).filter_by(address=address).one()

        return addr_obj.id
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        session.rollback()
        return None


def __save_batch(session, transactions_to_insert, thread_id, clear_batch=False):
    try:
        session.bulk_save_objects(transactions_to_insert)
        session.commit()
        __log_with_thread_id("Inserted records successfully.", thread_id)
        if clear_batch: transactions_to_insert.clear()
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Duplicate key error occurred while inserting transactions: {e}")
        match = re.search(r'\(hash\)=\((.*?)\)', str(e))
        if match:
            conflicting_hash = match.group(1)
            logger.error(f"Conflict detected for hash: {conflicting_hash}")
            conflicting_transactions = [tx for tx in transactions_to_insert if tx.hash == conflicting_hash]
            for tx in conflicting_transactions:
                logger.error(f"Conflicting transaction: {tx.hash}")
            existing_transaction = session.query(Transaction).filter_by(hash=conflicting_hash).first()
            if existing_transaction:
                logger.error(
                    "Existing transaction in database that caused the conflict: {}".format(existing_transaction))
    except Exception as e:
        logger.error(f"An unexpected error occurred while inserting transactions: {e}")
        session.rollback()


@app.command()
def ingest(address: str, starting_block: int, ending_block: int, thread_id: int):
    """
    Ingest data into the database from the API.
    - ingest from the api using specific startblock and endblock and an offset of 10000 (the current etherscan limit)
    - if the records are 10000 or more (a sign that there are more than 10000 records in between the startblock and the endblock), we dynmically reduce the endblock
    - if fewer than 10000 records, we batch and save to database
    """
    session = Session()
    transactions_to_insert = []
    current_block = starting_block
    block_window_amount = BASE_BLOCK_ATTEMPT

    try:
        while current_block <= ending_block:
            logger.info(f"New Loop. current_block: {current_block}, ending_block: {ending_block}, thread_id: {thread_id}")
            tentative_end_block = min(current_block + BASE_BLOCK_ATTEMPT, ending_block)
            data = __call_etherscan(address, thread_id, startblock=current_block, endblock=tentative_end_block)

            if not data["result"]:
                __log_with_thread_id(
                    f"Effing finally...Reached end of transactions for address: {address}, current_block: {current_block}, ending_block: {tentative_end_block}",
                    thread_id)
                break

            block_attempt_index = 0
            while len(data.get("result", [])) >= RECORD_RETRIEVAL_LIMIT:
                __log_with_thread_id(
                    f"thread_id: {thread_id}. Retrieved too many records with {block_window_amount}. Retrieved {len(data.get("result", []))} records.",
                    thread_id)
                block_window_amount = BLOCK_ATTEMPTS[block_attempt_index] if block_attempt_index < len(BLOCK_ATTEMPTS) else 20
                tentative_end_block = min(current_block + block_window_amount, ending_block)
                __log_with_thread_id(
                    f"Adjusting block range to {block_window_amount}, new end block: {tentative_end_block}", thread_id)
                data = __call_etherscan(address,  thread_id, startblock=current_block, endblock=tentative_end_block)
                block_attempt_index += 1

            __log_with_thread_id(
                f"Etherscan API call SUCCESS! Retrieved {len(data['result'])} records with a block window size of {block_window_amount}",
                thread_id)

            for tx in data["result"]:
                if int(tx["value"]) > 0 and tx["isError"] != "1":
                    from_address_id = __get_or_create_address(session, tx["from"])
                    to_address_id = __get_or_create_address(session, tx["to"])

                    transaction = Transaction(
                        block_number=int(tx["blockNumber"]),
                        time_stamp=datetime.fromtimestamp(int(tx["timeStamp"]), timezone.utc),
                        hash=tx["hash"],
                        from_address_id=from_address_id,
                        to_address_id=to_address_id,
                        value=int(tx["value"]),
                        gas=int(tx["gas"]),
                        gas_used=int(tx["gasUsed"]),
                        is_error=int(tx["isError"]),
                    )
                    transactions_to_insert.append(transaction)

            if len(transactions_to_insert) >= RECORD_RETRIEVAL_LIMIT:
                __save_batch(session, transactions_to_insert, thread_id, clear_batch=True)

            if data["result"]:
                __log_with_thread_id(f"Changing current block {current_block}", thread_id)
                current_block = int(data["result"][-1]["blockNumber"]) + 1
                __log_with_thread_id(f"New current block {current_block}", thread_id)
                block_window_amount = BASE_BLOCK_ATTEMPT

        # handle remaining transactions to insert
        __save_batch(session, transactions_to_insert, thread_id)
    except Exception as e:
        logger.error(f"Failed to ingest data: {e}")
        raise

    finally:
        session.close()


@app.command()
def crawl_and_ingest():
    logger.info(f"CONFIG: {CONFIG}")
    data = __call_etherscan(DEFAULT_ADDRESS, sort="asc")
    starting_block = int(data["result"][0]["blockNumber"])
    logger.info(f"Address starting_block: {starting_block}")

    if DEV_MODE:
        logger.info("IN DEV MODE, FAKE END BLOCK")
        ending_block = starting_block + THREADS_COUNT * DEV_MODE_ENDING_MULTIPLE
    else:
        data = __call_etherscan(DEFAULT_ADDRESS, sort="desc")
        ending_block = int(data["result"][0]["blockNumber"])
    logger.info(f"Address ending_block: {ending_block}")

    total_blocks = ending_block - starting_block + 1
    logger.info(f"Processing total blocks total on this run: {total_blocks}")
    blocks_per_thread = total_blocks // THREADS_COUNT
    logger.info(f"Processing total blocks per thread on this run: {blocks_per_thread}")

    with ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
        futures = []
        for i in range(THREADS_COUNT):
            thread_start_block = starting_block + i * blocks_per_thread
            thread_end_block = thread_start_block + blocks_per_thread - 1
            if i == THREADS_COUNT - 1:  # Ensure the last thread covers all remaining blocks
                thread_end_block = ending_block

            futures.append(executor.submit(ingest, DEFAULT_ADDRESS, thread_start_block, thread_end_block, i))

        [future.result() for future in futures]


if __name__ == "__main__":
    app()
