from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import  ChatOpenAI

import os
import tempfile


from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def create_pdf_embedings(pdf_file_path):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_bytes)  # write bytes to temp file
        temp_path = tmp_file.name
        loader = PyPDFLoader(temp_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " "],
        )
        chunks = text_splitter.split_documents(pages)
    return chunks


def create_pdf_embedings_dense(pdf_file_path):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_bytes)
        temp_path = tmp_file.name
        loader = PyPDFLoader(temp_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3800,
            chunk_overlap=300,
            length_function=len,
            separators=["\n\n", "\n", " "],
        )
        chunks = text_splitter.split_documents(pages)
    return chunks