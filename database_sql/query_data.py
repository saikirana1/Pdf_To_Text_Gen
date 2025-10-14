from .database_connection import get_session

from contextlib import contextmanager
from sqlmodel import select, text

from .models import Transaction,Invoice,Item,Account


@contextmanager
def get_db_session():
    yield from get_session()


def  query_data(query: str):
    print("------------->i am query data")
    try:
        with get_db_session() as session:
            query_str = str(query).strip().strip('"').strip("'")
            result = session.exec(text(query_str)).all()
        return result
    except Exception as e: 
        print(f"Database error: {e}")
        return "no data found"