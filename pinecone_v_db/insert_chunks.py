from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_cli
import uuid


def insert_chunks(chunks):
    db, table = get_db_table()
    table="pdf_chunks"
    pc = pinecone_cli()
    index = pc.Index(db)
    for chunk in chunks:
        print("Upserting item:", chunk.page_content)

        record = {"id": str(uuid.uuid4()), "description": chunk.page_content,"page_content":chunk.page_content,"source":chunk.metadata.get("source"),"page": chunk.metadata.get("page")}

        index.upsert_records(table, [record])
        print("Upserted into Pinecone:", record)

    print("All items upserted successfully!")
