from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import  ChatOpenAI

import os
import tempfile


from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def create_pdf_embedings(pdf_file):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    # t=llm.invoke("Tell me a joke about cats")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_path = tmp_file.name
    loader = PyPDFLoader(tmp_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,
                                            chunk_overlap=200,
                                            length_function=len,
                                            separators=["\n\n", "\n", " "])
    chunks = text_splitter.split_documents(pages)
    return chunks
