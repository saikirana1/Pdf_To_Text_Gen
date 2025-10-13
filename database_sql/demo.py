from sqlmodel import Session
from models import User, Account
from database_connection import get_session
from contextlib import contextmanager

@contextmanager
def get_db_session():
    yield from get_session()
with get_db_session() as session:
    print(session)
    user = User(email="sai2@example.com", hashed_password="hashedpassword123")
    session.add(user)
    session.commit()
