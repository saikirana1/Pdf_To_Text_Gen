from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import  ChatOpenAI

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

import os
import tempfile
import streamlit as st  
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def create_pdf_embedings():
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    # t=llm.invoke("Tell me a joke about cats")
    loader = PyPDFLoader("invoice-pdf/dl_base_paper.pdf")
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,
                                            chunk_overlap=200,
                                            length_function=len,
                                            separators=["\n\n", "\n", " "])
    chunks = text_splitter.split_documents(pages)
    return chunks
