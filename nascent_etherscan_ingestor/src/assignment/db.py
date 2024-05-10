from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.assignment.models import Base


def init_db(database_uri):
    engine = create_engine(database_uri)
    session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return session
