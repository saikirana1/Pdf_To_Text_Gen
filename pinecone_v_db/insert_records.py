from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_client
import uuid


def insert_records(items):
    db, table = get_db_table()
    pc = pinecone_client()
    index = pc.Index(db)

    for item in items:
        print("Upserting item:", item.get("description"))

        record = {"id": str(uuid.uuid4()), "description": item.get("description")}

        index.upsert_records(table, [record])
        print("Upserted into Pinecone:", record)

    print("All items upserted successfully!")
    return True
