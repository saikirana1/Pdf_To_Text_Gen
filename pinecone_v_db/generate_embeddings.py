from open_ai.client import openai_client
import os
from dotenv import load_dotenv

client = openai_client()

load_dotenv()

model = os.getenv("model")


def generate_embedding(text, model=model):
    try:
        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        print("embdding -----eroro", e)
