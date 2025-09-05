from .client import openai_client
import json
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

client = openai_client()


def pdf_to_json_data_extract(file):
    class BankStatements(BaseModel):
        transaction_id: Optional[str] = None
        transaction_date: Optional[str] = None
        withdrawal: Optional[float] = None
        deposit: Optional[float] = None
        balance: Optional[float] = None
        description: Optional[str] = None

    class BankStatementsData(BaseModel):
        transactions: List[BankStatements] = Field(default_factory=list)

    print("Process started...")

    completion = client.chat.completions.parse(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": file.id}},
                    {
                        "type": "text",
                        "text": """
                        You are an expert in extracting structured data from PDFs. 
                        Extract the PDF into a list of InvoiceData objects with the following fields:

                        here in this pdf names connect like this Transaction Date as transaction_date,transaction_id is not their put null,
                        Withdrawal as  withdrawal,Deposit as deposit,Balance as balance,Narration as description
                        here in this pdf date formate is date/month/year 
                        here don't put empty while in this pdf has data  
                        Rules:
                         - give the current date available in pdf table
                        - Map fields to InvoiceData as accurately as possible.
                       
                        - Return the result strictly following the InvoiceList structure.
                        """,
                    },
                ],
            }
        ],
        response_format=BankStatementsData,
    )

    result: BankStatementsData = completion.choices[0].message.parsed
    data = [item.model_dump() for item in result.transactions]

    return data
