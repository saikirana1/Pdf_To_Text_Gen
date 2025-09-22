from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_cli
import uuid


def insert_ice_cream_data(data):
    db, table = get_db_table()
    table="ice_cream_name"
    pc = pinecone_cli()
    index = pc.Index(db)
    records = data.get("result", [])
    for record in records:
        print("Upserting item:", record.get("item_name"))

        record_insert = {"id": str(uuid.uuid4()), "description": record.get("item_name"),"name":record.get("item_name")}

        index.upsert_records(table, [record_insert])
        print("Upserted into Pinecone:", record_insert)

    print("All items upserted successfully!")
    return True
