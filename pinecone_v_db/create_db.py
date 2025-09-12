from .pinecone_api_client import pinecone_client

from .get_db_table import get_db_table


client = pinecone_client()
index_name, table = get_db_table()


def create_db():
    if index_name not in client.list_indexes():
        client.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": "pinecone-sparse-english-v0",
                "field_map": {"text": "description"},
            },
        )

    return client.Index(index_name)
