from open_ai.openai_client import openai_client
import os

from dotenv import load_dotenv

client = openai_client()

load_dotenv()


model = os.getenv("model")


def create_embedding(text):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
