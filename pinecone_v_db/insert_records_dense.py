from .get_db_table import dense_get_db_table
from .pinecone_api_client import pinecone_cli
from .generate_embeddings import generate_embedding

import uuid


def insert_records_dense(chunks):
    try:
        db, table = dense_get_db_table()
        pc = pinecone_cli()
        index = pc.Index(db)
        vectors = []
        for chunk in chunks:
            vector = generate_embedding(chunk.page_content)
            record = {
                "id": str(uuid.uuid4()),
                "values": vector,
                "metadata": {
                    "description": chunk.page_content,
                    "page_content": chunk.page_content,
                    "source": chunk.metadata.get("source"),
                    "page": chunk.metadata.get("page"),
                },
            }
            print(chunk)
            vectors.append(record)

        t = index.upsert(vectors=vectors, namespace=table)
        print("Upserted successfully!")
    except Exception as e:
        print("Error====================", e)
    return t