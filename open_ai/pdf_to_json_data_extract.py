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

def pdf_to_json_data_extract(json_data,plain_text):

    print("Process started...")

    completion = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """
            You are an expert financial data extractor.
            Your job is to carefully analyze two json data
            and convert them into structured  provided schema.

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
                {
                    "type": "text",
                    "text": f"""
                   This data {json_data} is all transactions related data with out eliminating the one record 
                   return the required format based this messy data
                   in This data {plain_text} extract the account details only, if the required data missing put 
                   null
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
                    """,
                },
            ],
        },
    ],
    response_format=Result,
)

    parsed_result: Result = completion.choices[0].message.parsed
    json_result = parsed_result.model_dump_json(indent=4)
    print(json_result)
    print(type(json_result))
    data=json.loads(json_result)
    dict_result = parsed_result.model_dump()
    print(data)

    t=insert_data(data )
    # print(t)
   

    return dict_result
