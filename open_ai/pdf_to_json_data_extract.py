from .client import openai_client
import json
from pydantic import BaseModel, Field
from typing import List, Union

client = openai_client()


class Item(BaseModel):
    Description: str
    Qty: int
    UnitPrice: float
    Amount: float


class ChartData(BaseModel):
    label: str
    value: Union[float, int]


class PieChartData(BaseModel):
    label: str
    value: Union[float, int]


class BarChartData(BaseModel):
    label: str
    value: Union[float, int]


class InvoiceData(BaseModel):
    items: List[Item]
    subtotal: float
    sgst: float
    cgst: float
    total: float
    piechartdata: List[PieChartData] = Field(default_factory=list)
    barchartdata: List[BarChartData] = Field(default_factory=list)


def pdf_to_json_data_extract(file):
    completion = client.chat.completions.parse(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": file.id}},
                    {
                        "type": "text",
                        "text": """Extract the PDF into the InvoiceData format strictly.
                          here in this PieChartData for label is product name
                          and value is number of products and BarChartData label is product name and value is 
                          amount
                        """,
                    },
                ],
            }
        ],
        response_format=InvoiceData,
    )

    result: InvoiceData = completion.choices[0].message.parsed
    d = json.dumps(result.model_dump(), indent=2)
    data = json.loads(d)

    return data
