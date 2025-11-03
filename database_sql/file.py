from .database_connection import get_session

from contextlib import contextmanager
from .models import FileData
from datetime import date, datetime
from sqlmodel import select


@contextmanager
def get_db_session():
    yield from get_session()


def get_all_files_from_db():
    with get_db_session() as session:
        statement = select(FileData)
        return session.exec(statement).all()
    
def delete_file_from_db(file_id: str):
    with get_db_session() as session:
        try:
            file_record = session.get(FileData, file_id)
            if file_record:
                session.delete(file_record)
                session.commit()
                return file_record.id
            else:
                raise ValueError("File record not found")
        except Exception as e:
            print(f"Error deleting file record: {e}")
        return False
def insert_file_record(file_name: str, file_url: str, file_index: str = "") -> FileData:
    file_record = FileData(
        file_name=file_name, file_url=file_url, file_index=file_index
    )
    with get_db_session() as session:
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
    return file_record


        
