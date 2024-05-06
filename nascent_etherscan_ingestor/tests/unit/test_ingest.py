import pytest
from pytest_mock import MockerFixture
from concurrent.futures import Future
from src.assignment.ingest import crawl_and_ingest, ingest
from src.assignment.db import init_db
from src.assignment.models import Transaction, Address
from decimal import Decimal
from datetime import datetime

THREADS_IN_TEST = 4
SOME_DEFAULT_ADDRESS = 'some_default_address'


@pytest.fixture(autouse=True)
def mock_config_vars(mocker):
    mocker.patch('src.assignment.ingest.CONFIG', new={})
    mocker.patch('src.assignment.ingest.THREADS_COUNT', new=THREADS_IN_TEST)
    mocker.patch('src.assignment.ingest.DEV_MODE', new=None)
    mocker.patch('src.assignment.ingest.API_RATE_LIMIT_DELAY', new=0)
    mocker.patch('src.assignment.ingest.DATABASE_URI', new='some_fake_database_uri')
    mocker.patch('src.assignment.ingest.DEV_MODE_ENDING_MULTIPLE', new=20)
    mocker.patch('src.assignment.ingest.DEFAULT_ADDRESS', new=SOME_DEFAULT_ADDRESS)
    mocker.patch("src.assignment.ingest.API_KEY", new="some_api_key")
    mocker.patch("src.assignment.ingest.BASE_BLOCK_ATTEMPT", new=10)


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
def executor_mock(mocker):
    mock_executor = mocker.patch('src.assignment.ingest.ThreadPoolExecutor', autospec=True)
    mock_submit = mocker.Mock()
    future = Future()
    future.set_result(None)
    mock_submit.return_value = future
    # lol this took me forever to figure out how stub out the context manager's return_value
    mock_executor.return_value.__enter__.return_value.submit = mock_submit
    return mock_executor, mock_submit


@pytest.fixture
def ingest_mock(mocker):
    return mocker.patch('src.assignment.ingest.ingest')


class TestCrawlAndIngest:
    def test_api_calls_with_correct_parameters(self, mock_initial_requests_to_get_block_window, executor_mock, ingest_mock):
        expected_asc_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address=some_default_address&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey=some_api_key"
        expected_desc_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address=some_default_address&startblock=0&endblock=99999999&page=1&offset=10000&sort=desc&apikey=some_api_key"

        crawl_and_ingest()

        assert mock_initial_requests_to_get_block_window.call_args_list[0][0][0] == expected_asc_url
        assert mock_initial_requests_to_get_block_window.call_args_list[1][0][0] == expected_desc_url

    def test_threads_return(self, mock_initial_requests_to_get_block_window, executor_mock, ingest_mock):
        _, mock_submit = executor_mock

        crawl_and_ingest()

        # all futures are resolved
        assert all(call.return_value.result.called for call in mock_submit.call_args_list)

    def test_thread_execution_with_correct_block_ranges(self, mock_initial_requests_to_get_block_window, executor_mock, ingest_mock):
        mock_executor, _ = executor_mock
        expected_block_ranges_per_thread = [(1, 2), (3, 4), (5, 6), (7, 8)]

        crawl_and_ingest()

        actual_ranges = [
            (call.args[2], call.args[3]) for call in  mock_executor.return_value.__enter__.return_value.submit.call_args_list
        ]
        assert expected_block_ranges_per_thread == actual_ranges


class TestIngest:
    # you can test messages sent to the api OR test a test database. I think the latter is better and more stable for refactors.
    def test_ingest_simple_result_less_than_10k(self, mock_initial_requests_to_get_block_window, mock_db_session):
        starting_block = 0
        ending_block = 20
        thread_id = 0
        session = mock_db_session()
        expected_calls = [
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=0&endblock=10&page=1&offset=10000&sort=asc&apikey=some_api_key",
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=7&endblock=17&page=1&offset=10000&sort=asc&apikey=some_api_key",
            f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={SOME_DEFAULT_ADDRESS}&startblock=8&endblock=18&page=1&offset=10000&sort=asc&apikey=some_api_key",
        ]

        ingest(SOME_DEFAULT_ADDRESS, starting_block, ending_block, thread_id)

        # Check that the call count matches the expected number of API calls
        assert len(mock_initial_requests_to_get_block_window.call_args_list) == len(
            expected_calls), "Unexpected number of calls to requests.get"
        # Check each call against expected
        for call, expected_url in zip(mock_initial_requests_to_get_block_window.call_args_list, expected_calls):
            actual_url = call[0][0]
            assert actual_url == expected_url, f"Expected {expected_url}, got {actual_url}"

        assert session.bulk_save_objects.called, "Session.bulk_save_objects() was not called"
        assert session.commit.called, "Session.commit() was not called"
        assert session.close.called, "Session.close() was not called"

    def test_ingest_simple_result_less_than_10k_better_test(self, mock_initial_requests_to_get_block_window, test_db):
        starting_block = 0
        ending_block = 20
        thread_id = 1
        expected_valid_no_error_value_rows = [
      {
          'block_number': 1,
          'from_address_id': 1,
          'gas': 401,
          'gas_used': 500,
          'hash': 'some_hash_1',
          'id': 1,
          'is_error': 0,
          'time_stamp': datetime(1970, 1, 1, 0, 1, 41),
          'to_address_id': 1,
          'value': Decimal('200'),
      },
      {
          'block_number': 2,
          'from_address_id': 2,
          'gas': 402,
          'gas_used': 502,
          'hash': 'some_hash_2',
          'id': 2,
          'is_error': 0,
          'time_stamp': datetime(1970, 1, 1, 0, 1, 42),
          'to_address_id': 2,
          'value': Decimal('202'),
      },
      {
          'block_number': 3,
          'from_address_id': 3,
          'gas': 403,
          'gas_used': 503,
          'hash': 'some_hash_3',
          'id': 3,
          'is_error': 0,
          'time_stamp': datetime(1970, 1, 1, 0, 1, 43),
          'to_address_id': 3,
          'value': Decimal('203'),
      },
      {
          'block_number': 4,
          'from_address_id': 4,
          'gas': 404,
          'gas_used': 504,
          'hash': 'some_hash_4',
          'id': 4,
          'is_error': 0,
          'time_stamp': datetime(1970, 1, 1, 0, 1, 44),
          'to_address_id': 5,
          'value': Decimal('204'),
      },
      {
          'block_number': 8,
          'from_address_id': 6,
          'gas': 407,
          'gas_used': 507,
          'hash': 'some_hash_8',
          'id': 5,
          'is_error': 0,
          'time_stamp': datetime(1970, 1, 1, 0, 1, 48),
          'to_address_id': 6,
          'value': Decimal('208'),
      },
  ]

        ingest(SOME_DEFAULT_ADDRESS, starting_block, ending_block, thread_id)

        transactions = test_db.query(Transaction).all()
        actual = [{column.name: getattr(t, column.name) for column in t.__table__.columns} for t in transactions]

        # inspect the state of the in memory sqllite database, this is less brittle
        assert len(transactions) == 5, "Some wrong transactions were missed or  added."
        assert actual == expected_valid_no_error_value_rows



