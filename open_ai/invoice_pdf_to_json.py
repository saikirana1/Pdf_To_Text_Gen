from .client import openai_client
import json
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from database_sql.insert_invoice_data import insert_invoice_data

client = openai_client()


class Item(BaseModel):
    item_name: Optional[str] = None
    hsn_code: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    unit_taxable_amount: Optional[float] = None
    tax: Optional[str] = None
    unit_tax_amount: Optional[float] = None
    amount: Optional[float] = None
    mrp_price: Optional[float] = None


class BankDetails(BaseModel):
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    branch: Optional[str] = None


class Seller(BaseModel):
    address: Optional[str] = None
    contact: Optional[str] = None
    gst_number: Optional[str] = None
    fssai_no: Optional[str] = None
    pin_code: Optional[str] = None


class Payment(BaseModel):
    sub_total: Optional[float] = None
    s_gst: Optional[float] = None
    c_gst: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None


class Customer(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None


class Invoice(BaseModel):
    invoice_no: Optional[str] = None
    invoice_date: Optional[date] = None

    items: List[Item] = []
    bank_details: List[BankDetails] = []
    sellers: List[Seller] = []
    payments: List[Payment] = []
    customers: List[Customer] = []


class Result(BaseModel):
    result: List[Invoice]


def invoice_pdf_json(file_path):
    with open(file_path, "rb") as f:
        file = client.files.create(file=f, purpose="user_data")

        print("Process started...")

        completion = client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                You are an expert financial data extractor.
                Your job is to carefully analyze invoice pdf
                and convert them into structured  provided schema
                if value is unavailable Then put null.

                Rules:
                - Map fields accurately even if headings differ.
                - If data is missing, set it as null (do not hallucinate).
                - Be consistent in date formatting (YYYY-MM-DD).
                """,
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "file", "file": {"file_id": file.id}},
                        {
                            "type": "text",
                            "text": """
                    This pdf data is invoice related data with out eliminating the one record 
                    return the required format based this messy data
                        """,
                        },
                    ],
                },
            ],
            response_format=Result,
        )

        parsed_result: Result = completion.choices[0].message.parsed
        dict_result = parsed_result.model_dump()
        t = insert_invoice_data(dict_result)
        print(t, "===================>data inseted")
        print(dict_result, "dict_result====================================>")

    return dict_result
