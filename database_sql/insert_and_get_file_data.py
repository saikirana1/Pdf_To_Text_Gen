from .database_connection import get_session

from contextlib import contextmanager
from .models import FileData
from datetime import date, datetime
from sqlmodel import select


@contextmanager
def get_db_session():
    yield from get_session()


def insert_file_record(file_name: str, file_url: str, file_index: str = "") -> FileData:
    file_record = FileData(
        file_name=file_name, file_url=file_url, file_index=file_index
    )
    with get_db_session() as session:
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
    return file_record


def get_all_files_from_db():
    """
    Fetch all uploaded files from the database.
    """
    with get_db_session() as session:
        statement = select(FileData)
        files = session.exec(statement).all()
        return [
            {
                "id": f.id,
                "file_name": f.file_name,
                "file_url": f.file_url,
                "file_index": f.file_index,
            }
            for f in files
        ]
