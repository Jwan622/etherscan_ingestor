import pytest
from src.assignment.models import Base
from src.assignment.db import init_db


@pytest.fixture
def mock_create_engine(mocker):
    mock_created_engine = mocker.Mock()
    mock_create_engine = mocker.patch('src.assignment.db.create_engine', return_value=mock_created_engine)

    return mock_created_engine, mock_create_engine

@pytest.fixture
def mock_create_all(mocker):
    return mocker.patch.object(Base.metadata, 'create_all')


def test_init_db(mock_create_engine, mock_create_all):
    mock_created_engine, mock_create_engine = mock_create_engine
    test_url = 'test_url'

    init_db(test_url)

    mock_create_engine.assert_called_once_with(test_url)
    mock_create_all.assert_called_once_with(mock_created_engine)
