from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_cli
import uuid


def query_check(text: str):
    db, table = get_db_table()
    table="pdf_chunks"
    pc = pinecone_cli()
    index = pc.Index(db)

    results = index.search(
        namespace=table,
        query={"inputs": {"text": text}, "top_k": 1},
    )
    return results
