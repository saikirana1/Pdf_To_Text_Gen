import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from agents import Runner, Agent  

load_dotenv()

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

def pdf_to_text_extract(pdf_data: str) -> Result:
    data_extract = Agent(
        name="Pdf_to_Text",
        handoff_description=f"""
            You will extract the data {pdf_data} into the structured format below.
            Headings may differ in the PDF, so infer the best mapping.
            Expected format: accounts and transactions.if their is no available data 
            Then put the null don't put invalid data be carefully understand some times their is 
            no transaction id take care
        """,
        instructions="You provide help as a specialist agent for extracting structured data.",
        output_type=Result,
        model="gpt-4o-mini",
        
    )

    allocator_agent = Agent(
        name="Allocator Agent",
        instructions="Run the Agent for the Synthesizing data",
        handoffs=[data_extract],
    )

    result = asyncio.run(
        Runner.run(
            allocator_agent,
            "Extract and structure the data from PDF."
        )
    )

    print(result.final_output)
    return result.final_output
