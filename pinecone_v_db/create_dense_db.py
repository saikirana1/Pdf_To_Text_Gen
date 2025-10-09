from pinecone import ServerlessSpec
from .pinecone_api_client import pinecone_cli
from .get_db_table import dense_get_db_table


def dense_create_or_get_db():
    pinecone = pinecone_cli()
    db_name, table_name = dense_get_db_table()
    if db_name not in pinecone.list_indexes().names():
        pinecone.create_index(
            name=db_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index_name = pinecone.Index(
        name=db_name,
        pool_threads=50,
        connection_pool_maxsize=50,
    )
    return index_name
