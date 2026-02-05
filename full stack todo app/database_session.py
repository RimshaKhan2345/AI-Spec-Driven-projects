from sqlmodel import Session
from contextlib import contextmanager
from database import engine


def get_session():
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def get_session_direct():
    """Direct function to get a session, useful for dependency injection"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()