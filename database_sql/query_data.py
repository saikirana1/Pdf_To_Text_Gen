from .database_connection import get_session

from contextlib import contextmanager
from sqlmodel import select, text

from .models import Transaction


@contextmanager
def get_db_session():
    yield from get_session()


def query_data(query: str):
    with get_db_session() as session:
        query_str = str(query).strip().strip('"').strip("'")
        result = session.exec(text(query_str)).all()
    return result
