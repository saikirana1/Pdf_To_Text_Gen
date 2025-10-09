from .pinecone_api_client import pinecone_cli
import os

from dotenv import load_dotenv

client = pinecone_cli()

load_dotenv()

model = os.getenv("model")


def generate_embedding(text, model=model):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
