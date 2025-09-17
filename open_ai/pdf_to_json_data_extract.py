from .client import openai_client
import json
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from database_sql.insert_invoice_data import insert_invoice_data
client = openai_client()

class Item(BaseModel):
    invoice_date: Optional[date] = None
    invoice_no:  Optional[str] = None
    item_name: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    unit_taxable_amount: Optional[float] = None
    tax:  Optional[str]=None
    unit_tax_amount:  Optional[float] = None
    amount: Optional[float] = None
    mrp_price:Optional[float] = None
    gst_number:Optional[str] = None


class Result(BaseModel):
      result:List[Item]
   

def pdf_to_json_data_extract(file):

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
    # json_result = parsed_result.model_dump_json(indent=4)
    # print(json_result)
    # print(type(json_result))
    # data=json.loads(json_result)
    dict_result = parsed_result.model_dump()
    t=insert_invoice_data(dict_result)
    print(t)
    # print(data)

    # t=insert_data(data )
    # # print(t)
   

    return dict_result
