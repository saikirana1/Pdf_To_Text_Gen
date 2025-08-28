import base64
from pydantic import BaseModel
from typing import List
from client import openai_client
import json

client = openai_client()


class Product(BaseModel):
    name: str
    count: int


class ProductList(BaseModel):
    items: List[Product]
    total_count: int


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


image_path = "../product_images/11-products.png"
base64_image = encode_image(image_path)

completion = client.chat.completions.parse(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "what are the products are their in this image and count based on this response format give.and total count of products",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    response_format=ProductList,
)

result: ProductList = completion.choices[0].message.parsed


print(json.dumps(result.model_dump(), indent=2))
