from pinecone_v_db.create_db import create_db
from pinecone_v_db.insert_records import insert_records
import json
from pinecone_v_db.query_text import query_text
from pinecone_v_db.file_search import main
# db_create = create_db()

# print(db_create)


# with open("json_data/cleaned_data.json", "r") as f:
#     data = json.load(f)
#     insert_data = insert_records(data)


t = query_text("From:0706108700000029:STARCHIK FOODS PRIVATE LIMIT")
print(t)


# import asyncio

# asyncio.run(main())
