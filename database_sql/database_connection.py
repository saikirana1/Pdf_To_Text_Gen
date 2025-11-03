from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True,pool_pre_ping=True,pool_recycle=3600)


def get_session():
    with Session(engine) as session:
        yield session
