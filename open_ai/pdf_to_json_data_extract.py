from .client import openai_client
import json
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from database_sql.insert_data import insert_data
client = openai_client()

class Account(BaseModel):
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    name: Optional[str] = None

class Transaction(BaseModel):
    transaction_id: Optional[str] = None
    transaction_date: Optional[date] = None
    withdrawal: Optional[float] = None
    deposit: Optional[float] = None
    balance: Optional[float] = None
    description: Optional[str] = None
    check_number: Optional[str] = None

class Result(BaseModel):
    account: List[Account]
    transactions: List[Transaction]

def pdf_to_json_data_extract(file):

    print("Process started...")

    completion = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """
            You are an expert financial data extractor.
            Your job is to carefully analyze PDFs (like bank statements or invoices)
            and convert them into structured JSON following the provided schema.

            Rules:
            - Map fields accurately even if headings differ.
            - If data is missing, set it as null (do not hallucinate).
            - Be consistent in date formatting (YYYY-MM-DD).
            - Ensure withdrawals, deposits, and balances are numbers (float).
            - Keep transaction_id null if not available, don’t make one up.
            - must fill the balance if not in their then null 
            """,
        },
        {
            "role": "user",
            "content": [
                {"type": "file", "file": {"file_id": file.id}},
                {
                    "type": "text",
                    "text": """
                    Extract the data into the structured format (Result model).
                    Return strictly valid JSON that matches the schema.
                    some times you are giving invalid data options
                    This is my data model
                    class Account(BaseModel):
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    name: Optional[str] = None

class Transaction(BaseModel):
    transaction_id: Optional[str] = None
    transaction_date: Optional[date] = None
    withdrawal: Optional[float] = None
    deposit: Optional[float] = None
    balance: Optional[float] = None
    description: Optional[str] = None
    check_number: Optional[str] = None

class Result(BaseModel):
    account: List[Account]
    transactions: List[Transaction]
    don't miss the balance and deposit
    you are missing it ,please make sure put the balance
                    """,
                },
            ],
        },
    ],
    response_format=Result,
)

    result: Result = completion.choices[0].message.parsed.model_dump_json(indent=4)
    data=json.loads(result)
    t=insert_data(data)
    print(t)
   
    return data
