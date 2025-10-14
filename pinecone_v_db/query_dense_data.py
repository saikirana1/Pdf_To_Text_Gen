import os
from .generate_embeddings import generate_embedding
from .get_db_table import dense_get_db_table
from dotenv import load_dotenv
from .pinecone_api_client import pinecone_cli

load_dotenv()


def filter_records(quation):
    pc = pinecone_cli()

    db, table_name = dense_get_db_table()

    index = pc.Index(db)

    vector = generate_embedding(quation)
    response = index.query(
        vector=vector,
        namespace=table_name,
        top_k=1,
        include_metadata=True,
        include_values=False,
    )
