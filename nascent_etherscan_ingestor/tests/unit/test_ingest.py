import pytest
from pytest_mock import MockerFixture
from concurrent.futures import Future
from src.assignment.ingest import start, call_api_and_produce
from src.assignment.db import init_db
from datetime import datetime
import datetime

PRODUCER_THREAD_COUNT = 4
SOME_DEFAULT_ADDRESS = 'some_default_address'


@pytest.fixture(autouse=True)
def mock_config_vars(mocker):
    mocker.patch('src.assignment.ingest.CONFIG', new={})
    mocker.patch("src.assignment.ingest.API_KEY", new="some_api_key")
    mocker.patch('src.assignment.ingest.API_RATE_LIMIT_DELAY', new=0)
    mocker.patch("src.assignment.ingest.BASE_BLOCK_ATTEMPT", new=4)
    mocker.patch('src.assignment.ingest.DEFAULT_ADDRESS', new=SOME_DEFAULT_ADDRESS)
    mocker.patch('src.assignment.ingest.DEV_MODE', new=None)
    mocker.patch('src.assignment.ingest.DATABASE_URI', new='some_fake_database_uri')
    mocker.patch("src.assignment.ingest.SAVE_BATCH_LIMIT", new=3)
    mocker.patch('src.assignment.ingest.PRODUCER_THREAD_COUNT', new=PRODUCER_THREAD_COUNT)


@pytest.fixture
def mock_db_session(mocker):
    test_session = init_db('sqlite:///:memory:')

    session_mock = mocker.MagicMock(spec=test_session)
    mock_add = mocker.Mock()
    mock_commit = mocker.Mock()
    mock_rollback = mocker.Mock()
    mock_close = mocker.Mock()
    mock_bulk_save_object = mocker.Mock()
    query_mock = mocker.Mock()
    filter_mock = mocker.Mock()
    addr_obj_mock = mocker.Mock()
    addr_obj_mock.id = 123

    session_mock.add = mock_add
    session_mock.commit = mock_commit
    session_mock.bulk_save_objects = mock_bulk_save_object
    session_mock.rollback = mock_rollback
    session_mock.close = mock_close

    query_mock.filter_by.return_value = filter_mock
    session_mock.query.return_value = query_mock
    filter_mock.one_or_none.return_value = addr_obj_mock

    mocker.patch('src.assignment.ingest.Session', new_callable=lambda: session_mock)
    return session_mock


@pytest.fixture
def test_db(mocker):
    test_session = init_db('sqlite:///:memory:')
    mocker.patch('src.assignment.ingest.Session', new_callable=lambda: test_session)
    return test_session


@pytest.fixture
def mock_transaction(mocker):
    return mocker.patch('src.assignment.ingest.Transaction', autospec=True)


@pytest.fixture
def mock_initial_requests_to_get_block_window(mocker: MockerFixture):
    response_mock_asc = mocker.Mock()
    response_mock_asc.json.return_value = {
        "status": "1",
        "message": "OK",
        "result": [
            {
                "blockNumber":"1","timeStamp":"101","hash":"some_hash_1","from":"some_from_address_1",
                "to":"some_from_address_1","value":"200","contractAddress":"some_contract_Address1","input":"",
                "type":"call","gas":"401","gasUsed":"500","traceId":"0_2_0","isError":"0","errCode":""
            },
            {
                "blockNumber": "2", "timeStamp": "102", "hash": "some_hash_2", "from": "some_from_address_2",
                "to": "some_from_address_2", "value": "202", "contractAddress": "some_contract_Address2", "input": "",
                "type": "call", "gas": "402", "gasUsed": "502", "traceId": "0_2_0", "isError": "0", "errCode": ""
            },
            {
                "blockNumber": "3", "timeStamp": "103", "hash": "some_hash_3", "from": "some_from_address_3",
                "to": "some_from_address_3", "value": "203", "contractAddress": "some_contract_Address3", "input": "",
                "type": "call", "gas": "403", "gasUsed": "503", "traceId": "0_2_0", "isError": "0", "errCode": ""
            },
            {
                "blockNumber": "4", "timeStamp": "104", "hash": "some_hash_4", "from": "some_from_address_5",
                "to": "some_from_address_4", "value": "204", "contractAddress": "some_contract_Address4", "input": "",
                "type": "call", "gas": "404", "gasUsed": "504", "traceId": "0_2_0", "isError": "0", "errCode": ""
            },
            {
                "blockNumber": "5", "timeStamp": "105", "hash": "some_hash_5", "from": "some_from_address_5",
                "to": "some_from_address_4", "value": "0", "contractAddress": "some_contract_Address5", "input": "",
                "type": "call", "gas": "405", "gasUsed": "505", "traceId": "0_2_0", "isError": "0", "errCode": ""
            },
            {
                "blockNumber": "6", "timeStamp": "106", "hash": "some_hash_6", "from": "some_from_address_6",
                "to": "some_from_address_6", "value": "206", "contractAddress": "some_contract_Address6", "input": "",
                "type": "call", "gas": "406", "gasUsed": "506", "traceId": "0_2_0", "isError": "1", "errCode": ""
            }
        ]
    }

    response_mock_desc = mocker.Mock()
    response_mock_desc.json.return_value = {
        "status": "1",
        "message": "OK",
        "result": [
            {
                "blockNumber": "8", "timeStamp": "108", "hash": "some_hash_8", "from": "some_from_address_8",
                "to": "some_from_address_8", "value": "208", "contractAddress": "some_contract_Address8",
                "input": "",
                "type": "call", "gas": "407", "gasUsed": "507", "traceId": "0_2_0", "isError": "0", "errCode": "0"
            },
            {
                "blockNumber": "7", "timeStamp": "107", "hash": "some_hash_7", "from": "some_from_address_7",
                "to": "some_from_address_7", "value": "207", "contractAddress": "some_contract_Address17",
                "input": "",
                "type": "call", "gas": "407", "gasUsed": "507", "traceId": "0_2_0", "isError": "1", "errCode": "1"
            }
        ]
    }

    empty_response = mocker.Mock()
    empty_response.json.return_value = {
        "status": "1",
        "message": "OK",
        "result": []
    }

    return mocker.patch('src.assignment.ingest.requests.get', side_effect=[response_mock_asc, response_mock_desc, empty_response])


@pytest.fixture
def mock_etherscan_calls_for_blocks(mocker: MockerFixture):
    last_block_number = [0]  # Using a list to hold the counter to avoid nonlocal declaration issues

    def create_response(block_start, count=2):
        return {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "blockNumber": str(block_start + i),
                    "timeStamp": str(100 + block_start + i),
                    "hash": f"some_hash_{block_start + i}",
                    "from": f"some_from_address_{block_start + i}",
                    "to": f"some_to_address_{block_start + i}",
                    "value": str(200 + block_start + i),
                    "contractAddress": f"some_contract_address_{block_start + i}",
                    "input": "",
                    "type": "call",
                    "gas": str(400 + block_start + i),
                    "gasUsed": str(500 + block_start + i),
                    "traceId": "0_2_0",
                    "isError": "0",
                    "errCode": ""
                } for i in range(count)
            ]
        }

    def response_function(url, params=None):
        response = mocker.Mock()
        response.json.return_value = create_response(last_block_number[0])
        last_block_number[0] += 2
        return response


    return mocker.patch('src.assignment.ingest.requests.get', side_effect=response_function)



@pytest.fixture
def executor_mock(mocker):
    mock_executor = mocker.patch('src.assignment.ingest.ThreadPoolExecutor', autospec=True)
    mock_submit = mocker.Mock()
    # lol this took me forever to figure out how stub out the context manager's return_value
    mock_executor.return_value.__enter__.return_value.submit = mock_submit
    future = Future()
    future.set_result(None)
    mock_submit.return_value = future
    return mock_executor, mock_submit


@pytest.fixture
def mock_call_api_and_produce(mocker):
    return mocker.patch('src.assignment.ingest.call_api_and_produce')

@pytest.fixture
def mock_consume(mocker):
    return mocker.patch('src.assignment.ingest.consume')


@pytest.fixture
def mock_queue(mocker):
    mock_queue = mocker.Mock()
    mocker.patch('src.assignment.ingest.queue.Queue', return_value=mock_queue)
    return mock_queue


@pytest.fixture
def mock_threading_event(mocker):
    mock_threading_event = mocker.Mock()
    mocker.patch('src.assignment.ingest.threading.Event', return_value=mock_threading_event)
    return mock_threading_event


class TestStart:
    def test_correctly_makes_two_api_calls_to_get_block_window(self, mock_initial_requests_to_get_block_window, executor_mock,
                                                               mock_call_api_and_produce):
        expected_asc_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address=some_default_address&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey=some_api_key"
        expected_desc_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address=some_default_address&startblock=0&endblock=99999999&page=1&offset=10000&sort=desc&apikey=some_api_key"

        start()

        assert mock_initial_requests_to_get_block_window.call_args_list[0][0][0] == expected_asc_url
        assert mock_initial_requests_to_get_block_window.call_args_list[1][0][0] == expected_desc_url

    def test_submit_consumer_and_producer_threads(self, mocker, mock_initial_requests_to_get_block_window, executor_mock,
                                                  mock_call_api_and_produce, mock_queue, mock_threading_event, mock_consume):
        _, mock_submit = executor_mock
        expected_calls = [
            mocker.call(mock_consume, mock_queue, mock_threading_event),
            mocker.call(mock_call_api_and_produce, 'some_default_address', 1, 4, mock_queue, 0),
            mocker.call(mock_call_api_and_produce, 'some_default_address', 5, 8, mock_queue, 1),
        ]

        start()

        mock_submit.assert_has_calls(expected_calls)

    def test_producer_threads_called_with_correct_block_ranges(self, mock_initial_requests_to_get_block_window, executor_mock,
                                                        mock_call_api_and_produce):
        mock_executor, _ = executor_mock
        expected_block_ranges_per_thread = [(1, 4), (5, 8)]

        start()

        actual_ranges = [
            (call.args[2], call.args[3]) for call in  mock_executor.return_value.__enter__.return_value.submit.call_args_list[1:] # only the producers
        ]
        assert expected_block_ranges_per_thread == actual_ranges


class TestCallApiAndProduce:
    def test_calls_api_with_correct_blocks(self, mock_etherscan_calls_for_blocks, mock_queue, mock_db_session):
        starting_block = 0
        ending_block = 20
        thread_id = 0
        expected_calls = [
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=0&endblock=4&page=1&offset=10000&sort=asc&apikey=some_api_key",
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=5&endblock=9&page=1&offset=10000&sort=asc&apikey=some_api_key",
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=10&endblock=14&page=1&offset=10000&sort=asc&apikey=some_api_key",
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=15&endblock=19&page=1&offset=10000&sort=asc&apikey=some_api_key",
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=20&endblock=20&page=1&offset=10000&sort=asc&apikey=some_api_key",
        ]

        call_api_and_produce(SOME_DEFAULT_ADDRESS, starting_block, ending_block, mock_queue, thread_id)

        assert len(mock_etherscan_calls_for_blocks.call_args_list) == len(
            expected_calls), "Unexpected number of calls to requests.get"
        for call, expected_url in zip(mock_etherscan_calls_for_blocks.call_args_list, expected_calls):
            actual_url = call[0][0]
            assert actual_url == expected_url, f"Expected {expected_url}, got {actual_url}"

    def test_call_api_with_correct_blocks_with_mock_queue(self, mock_etherscan_calls_for_blocks, mock_queue, mock_transaction, test_db):
        starting_block = 0
        ending_block = 20
        thread_id = 1
        expected_transaction_calls = [
            {'block_number': 0, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 40, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_0', 'from_address_id': 1, 'to_address_id': 2, 'value': 200,'gas': 400, 'gas_used': 500, 'is_error': 0},
            {'block_number': 1, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 41, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_1', 'from_address_id': 3, 'to_address_id': 4, 'value': 201,  'gas': 401, 'gas_used': 501, 'is_error': 0},
            {'block_number': 2, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 42, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_2', 'from_address_id': 5, 'to_address_id': 6, 'value': 202, 'gas': 402, 'gas_used': 502, 'is_error': 0},
            {'block_number': 3, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 43, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_3', 'from_address_id': 7, 'to_address_id': 8, 'value': 203, 'gas': 403, 'gas_used': 503, 'is_error': 0},
            {'block_number': 4, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 44, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_4', 'from_address_id': 9, 'to_address_id': 10, 'value': 204, 'gas': 404, 'gas_used': 504, 'is_error': 0},
            {'block_number': 5, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 45, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_5', 'from_address_id': 11, 'to_address_id': 12, 'value': 205, 'gas': 405, 'gas_used': 505, 'is_error': 0},
            {'block_number': 6, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 46, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_6', 'from_address_id': 13, 'to_address_id': 14, 'value': 206, 'gas': 406, 'gas_used': 506, 'is_error': 0},
            {'block_number': 7, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 47, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_7', 'from_address_id': 15, 'to_address_id': 16, 'value': 207, 'gas': 407, 'gas_used': 507, 'is_error': 0},
            {'block_number': 8, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 48, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_8', 'from_address_id': 17, 'to_address_id': 18, 'value': 208, 'gas': 408, 'gas_used': 508, 'is_error': 0},
            {'block_number': 9, 'time_stamp': datetime.datetime(1970, 1, 1, 0, 1, 49, tzinfo=datetime.timezone.utc), 'hash': 'some_hash_9', 'from_address_id': 19, 'to_address_id': 20, 'value': 209, 'gas': 409, 'gas_used': 509, 'is_error': 0}
        ]

        call_api_and_produce(SOME_DEFAULT_ADDRESS, starting_block, ending_block, mock_queue, thread_id)

        for call, expected in zip(mock_transaction.call_args_list, expected_transaction_calls):
            _, kwargs = call

            for key, val in expected.items():
                assert kwargs[key] == val

        assert len(mock_queue.put.call_args_list) == 10 # all the transactions are mocks and the same.
