from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_client
from .create_embedding import create_embedding


def insert_records(items):
    db, table = get_db_table()
    pc = pinecone_client()
    index = pc.Index(db)

    for item in items:
        print(item)

        vector = create_embedding(item["name"])

        record = (
            item["id"],
            vector,
            {"product_name": item["name"]},
        )

        index.upsert(vectors=[record], namespace=table)
        print("upserted into pinecone")
    print("Upserted successfully!")
    return True
