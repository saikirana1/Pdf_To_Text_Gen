from .get_db_table import dense_get_db_table
from .pinecone_api_client import pinecone_cli
from .generate_embeddings import generate_embedding

import uuid


def insert_records(text):
    db, table = dense_get_db_table()
    pc = pinecone_cli()
    index = pc.Index(db)
    vectors = []
    vector = generate_embedding(text)
    record = {
        "id": str(uuid.uuid4()),
        "values": vector,
        "metadata": {"title": item["dish"], "image_path": f"{item['id']}.png"},
    }
    vectors.append(record)

    t = index.upsert(vectors=vectors, namespace=table)
    print("Upserted successfully!")
    return t
