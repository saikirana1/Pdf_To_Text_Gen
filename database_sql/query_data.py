from .database_connection import get_session
from .models import Restaurant, Dishes
from contextlib import contextmanager
from sqlmodel import select
from .un_matched_records_table import UNMATCHEDRECORDS


@contextmanager
def get_db_session():
    yield from get_session()


def query():
    with get_db_session() as session:
        statement = select(Restaurant)
        restaurants = session.exec(statement).all()
        restaurants_with_id = [{"id": i.id, "name": i.name} for i in restaurants]
        print(restaurants_with_id)
