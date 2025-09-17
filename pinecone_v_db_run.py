# from pinecone_v_db.create_db import create_db
# from pinecone_v_db.insert_records import insert_records
# import json
# from pinecone_v_db.query_text import query_text
# from pinecone_v_db.file_search import main
# # from pinecone_v_db.delete_namespace import delete_namespace
# from open_ai.pdf_to_text_extract import pdf_to_text_extract
from open_ai.create_pdf_embedings import create_pdf_embedings
from pinecone_v_db.insert_chunks import insert_chunks
from pinecone_v_db.query_chunk import  query_check


# chunks=create_pdf_embedings()
# result=insert_chunks(chunks)
# print(result)
result=query_check("explain the summery of this")
print(result)