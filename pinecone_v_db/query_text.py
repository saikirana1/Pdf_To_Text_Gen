from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_client
import uuid


def query_text(text: str):
    db, table = get_db_table()
    pc = pinecone_client()
    index = pc.Index(db)

    results = index.search(
        namespace=table,
        query={"inputs": {"text": text}, "top_k": 1},
    )
    return results
