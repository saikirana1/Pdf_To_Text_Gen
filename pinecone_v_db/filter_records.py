import os
from pinecone_v_db.create_embedding import create_embedding
from pinecone_v_db.get_db_table import get_db_table
from dotenv import load_dotenv
from pinecone_v_db.pinecone_api_client import pinecone_client


def filter_records(items: list):
    load_dotenv()
    threshold = os.getenv("threshold")
    pc = pinecone_client()

    matched_records = []
    unmatched_records = []
    db, table_name = get_db_table()

    index = pc.Index(db)
    for item in items:
        vector = create_embedding(item)
        response = index.query(
            vector=vector,
            namespace=table_name,
            top_k=1,
            include_metadata=True,
            include_values=False,
        )

        matches = response.get("matches", [])
        if matches:
            match = matches[0]
            score = match.get("score", 0)

            if score >= float(threshold):
                metadata = match.get("metadata", {})
                matched_records.append(
                    {
                        "id": match.get("id"),
                        "product": item,
                        "product_name": metadata["product_name"],
                        "score": score,
                    }
                )

            else:
                unmatched_records.append(item)
        else:
            unmatched_records.append(item)
    return matched_records, unmatched_records
