import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.assignment.ingest import start, init_db
from dotenv import dotenv_values
import queue
from pytest_mock import MockerFixture

from src.assignment.models import Base, Transaction

CONFIG = dotenv_values(".env.test")
API_KEY = dotenv_values(".env")['API_KEY']


class TestIntegrationIngest():
    @pytest.fixture(autouse=True)
    def mock_config_vars(self, mocker):
        mocker.patch('src.assignment.ingest.CONFIG', new=CONFIG)
        mocker.patch("src.assignment.ingest.API_KEY", new=API_KEY)
        mocker.patch('src.assignment.ingest.RECORD_RETRIEVAL_LIMIT', new=100)
        mocker.patch('src.assignment.ingest.DEFAULT_ADDRESS', new='0xE592427A0AEce92De3Edee1F18E0157C05861564')
        mocker.patch('src.assignment.ingest.DATABASE_URI', new='some_fake_database_uri')
        mocker.patch('src.assignment.ingest.PRODUCER_THREAD_COUNT', new=4)
        mocker.patch('src.assignment.ingest.CONSUMER_THREAD_COUNT', new=1)
        mocker.patch('src.assignment.ingest.SEMAPHOR_THREAD_COUNT', new=4)
        mocker.patch('src.assignment.ingest.API_RATE_LIMIT_DELAY', new=0.1)
        mocker.patch('src.assignment.ingest.SAVE_BATCH_LIMIT', new=4)
        mocker.patch('src.assignment.ingest.BASE_BLOCK_ATTEMPT', new=8)
        mocker.patch('src.assignment.ingest.BLOCK_ATTEMPTS', new=[4,2,1])
        mocker.patch('src.assignment.ingest.DEV_MODE', new=None)
        mocker.patch('src.assignment.ingest.DEV_PRODUCER_THREAD_COUNT', new=4)
        mocker.patch('src.assignment.ingest.DEV_STEP', new=4)
        mocker.patch('src.assignment.ingest.DEV_MODE_ENDING_MULTIPLE', new=25)
        mocker.patch('src.assignment.ingest.TEST_MODE', new=CONFIG['TEST_MODE'])
        mocker.patch('src.assignment.ingest.TEST_MODE_STARTING_BLOCK', new=CONFIG['TEST_MODE_STARTING_BLOCK'])
        mocker.patch('src.assignment.ingest.TEST_MODE_END_BLOCK', new=CONFIG['TEST_MODE_END_BLOCK'])


    @pytest.fixture
    def mock_queue(self, mocker):
        mock_queue = queue.Queue()
        mocker.patch('src.assignment.ingest.queue.Queue', return_value=mock_queue)
        return mock_queue

    @pytest.fixture(scope='function')
    def init_test_db(self, mocker):
        engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        session_factory = scoped_session(sessionmaker(bind=engine))

        Base.metadata.create_all(engine)
        mocker.patch('src.assignment.ingest.Session', return_value=session_factory)
        return session_factory

    def test_multi_threaded_ingest(self, mock_config_vars, mock_queue, init_test_db):
        session_factory = init_test_db

        start()

        assert mock_queue.qsize() == 0

        with session_factory() as sesh:
            transaction_count = sesh.query(Transaction).count()
            assert transaction_count == 46 # this should never change because you can't alter the blockchain





