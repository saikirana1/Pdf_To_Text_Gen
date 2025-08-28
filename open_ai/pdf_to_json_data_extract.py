from .client import openai_client
import json

client = openai_client()


def pdf_to_json_data_extract(file):
    completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": file.id}},
                    {
                        "type": "text",
                        "text": """Extract invoice details as JSON dictionary with fields:
                        - items: list of dicts { "Description", "Qty", "UnitPrice", "Amount" }
                        - subtotal
                        - sgst
                        - cgst
                        - total
                        - piechartdata: list of dicts { "label": Description, "value": Qty }
                        - barchartdata: list of dicts { "label": Description, "value": Amount }
                        """,
                    },
                ],
            }
        ],
    )

    response_text = completion.choices[0].message.content

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        data = json.loads(response_text[start:end])
    return data
