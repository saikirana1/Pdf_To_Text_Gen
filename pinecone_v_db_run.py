from pinecone_v_db.create_db import create_db
from pinecone_v_db.insert_records import insert_records
import json
from pinecone_v_db.query_text import query_text
from pinecone_v_db.file_search import main
# from pinecone_v_db.delete_namespace import delete_namespace
from open_ai.pdf_to_text_extract import pdf_to_text_extract
# db_create = create_db()

# print(db_create)


# with open("json_data/cleaned_data.json", "r") as f:
#     data = json.load(f)
#     insert_data = insert_records(data)


# t = query_text("From:0706108700000029:STARCHIK FOODS PRIVATE LIMIT")
# print(t)

# t=delete_namespace()
# print(t)
# import asyncio

# asyncio.run(main())
import fitz  # PyMuPDF for reading PDF text

# Function to read PDF text
# def load_pdf_text(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text("text") + "\n"
#     return text.strip()

# # Example usage
# pdf_path = "invoice-pdf/p-1.pdf"   # 👈 replace with your file path
# pdf_text = load_pdf_text(pdf_path)

# # Now call your function that extracts structured data
# structured_data = pdf_to_text_extract(pdf_text)

# print("✅ Final structured data:")
# print(structured_data)
#  # Pydantic -> dict

data=[
{
    "transaction_data": "24/03/2025",
   
    "description": "NEFT_IN:null//ICICN52025032400471241/SALASA R TRADING COMPAN"
  },
  {
    "transaction_data": "20/03/2025",
   
    "description": "From:XXXX0029:STARCHIK FOODS PRIVATE LIMIT"
  },
  {
    "transaction_data": "14/03/2025",
  
    "description": "ATM ANN.CHRG FOR CARD-6615 YEAR ENDED 2024-25"
  }
]
t=insert_records(data)
print(t)