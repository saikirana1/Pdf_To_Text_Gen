from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_cli
import uuid
import json
import datetime
def insert_ice_cream_data(data):
    records = data.get("result", [])
    if not records:
        return "No data found from invoice rag insert"

    db, table = get_db_table()
    table="ice_cream_name"
    pc = pinecone_cli()
    index = pc.Index(db)
    invoice_no = records[0].get("invoice_no")
    print("Inserting invoice id is ", invoice_no)
    print("Upserting item:", data)

    t = json.dumps(records, indent=4, default=str)
    print(type(t), "-------------------------------===============================>")
    print(t)

    record_insert = {
        "id": str(uuid.uuid4()),
        "description": f"invoice id is {invoice_no}",
        "details": t,
    }

    index.upsert_records(table, [record_insert])
    print("Upserted into Pinecone:", record_insert)

    print("All items upserted successfully!")

