from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_client
import uuid


def insert_records(data):
    db, table = get_db_table()
    pc = pinecone_client()
    index = pc.Index(db)

    for txn in data.get("transactions", []):
        print("Upserting item:", txn.get("description"))

        record = {"id": str(uuid.uuid4()), "description": txn.get("description")}

        index.upsert_records(table, [record])
        print("Upserted into Pinecone:", record)

    print("All items upserted successfully!")
    return True
