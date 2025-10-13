# from open_ai.client import openai_client
# from pydantic import BaseModel

# client = openai_client()


# class AddInput(BaseModel):
#     a: int
#     b: int


# # Define strict function using decorator
# @client.tools.function
# def add_fn(data: AddInput) -> int:
#     """Add two numbers"""
#     return data.a + data.b


# class SubtractInput(BaseModel):
#     a: int
#     b: int


# @client.tools.function
# def subtract_fn(data: SubtractInput) -> int:
#     """Subtract second number from first number"""
#     return data.a - data.b


# # Tool definitions
# tools = [
#     {
#         "type": "function",
#         "strict": True,  # corrected typo
#         "function": {
#             "name": "add",
#             "description": "Add two numbers",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "a": {"type": "integer", "description": "First number"},
#                     "b": {"type": "integer", "description": "Second number"},
#                 },
#                 "required": ["a", "b"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "strict": True,
#         "function": {
#             "name": "subtract_numbers",
#             "description": "Subtract second number from first number",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "a": {"type": "integer", "description": "First number"},
#                     "b": {"type": "integer", "description": "Second number"},
#                 },
#                 "required": ["a", "b"],
#             },
#         },
#     },
# ]


# class Data(BaseModel):
#     value: int


# response = client.chat.completions.parse(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Add 10 and 5 given response format"}],
#     response_format=Data,
#     tools=[add_fn, subtract_fn],
# )

# print(response)


# import streamlit as st

# st.title("User Input Example")
# query = st.chat_input("Say something: ")


# import streamlit as st
# import openai
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Pinecone
# import pinecone

# # -----------------------
# # CONFIG
# # -----------------------
# openai.api_key = "your_openai_api_key_here"
# pinecone_api_key = "your_pinecone_api_key_here"
# pinecone_env = "your_pinecone_environment"  # e.g. "gcp-starter"

# # Initialize Pinecone
# pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

# # Name of index
# index_name = "pdf-rag-demo"

# # Create Pinecone index if not exists
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(
#         index_name, dimension=1536, metric="cosine"
#     )  # 1536 for OpenAI embeddings


# # -----------------------
# # FUNCTIONS
# # -----------------------
# def extract_text_from_pdf(uploaded_file):
#     """Extract text from uploaded PDF"""
#     reader = PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         if page.extract_text():
#             text += page.extract_text() + "\n"
#     return text


# def create_vectorstore(text):
#     """Split text into chunks and store in Pinecone"""
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = splitter.split_text(text)

#     embeddings = OpenAIEmbeddings()
#     vectorstore = Pinecone.from_texts(chunks, embeddings, index_name=index_name)
#     return vectorstore


# def answer_query(vectorstore, query):
#     """Retrieve relevant context and answer using OpenAI"""
#     docs = vectorstore.similarity_search(query, k=3)
#     context = "\n".join([d.page_content for d in docs])

#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",  # or "gpt-4o"
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant. Answer only using the provided PDF context.",
#             },
#             {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
#         ],
#         temperature=0,
#     )
#     return response.choices[0].message["content"]


# # -----------------------
# # STREAMLIT APP
# # -----------------------
# st.set_page_config(page_title="📄 PDF Q&A with Pinecone + RAG", layout="centered")

# st.title("📄 PDF Question Answering with Pinecone + OpenAI")
# st.write("Upload a PDF and then ask questions about it!")

# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# if uploaded_file is not None:
#     st.success("✅ PDF uploaded successfully!")

#     # Extract & create vectorstore once
#     with st.spinner("Processing PDF..."):
#         text = extract_text_from_pdf(uploaded_file)
#         vectorstore = create_vectorstore(text)
#     st.success("PDF processed and stored in Pinecone! 🎉")

#     # User input question
#     query = st.text_input("🔍 Ask a question about the PDF:")

#     if query:
#         with st.spinner("Thinking... 🤔"):
#             answer = answer_query(vectorstore, query)
#         st.subheader("📌 Answer:")
#         st.write(answer)


# import streamlit as st
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from openai import OpenAI
# import pinecone
# import hashlib
# import os

# # ---------------------
# # CONFIG
# # ---------------------
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")
# INDEX_NAME = "pdf-rag-demo"
# NAMESPACE = "custom-namespace"  # custom namespace for separating data

# # Initialize clients
# client = OpenAI(api_key=OPENAI_API_KEY)
# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# index = pinecone.Index(INDEX_NAME)


# # ---------------------
# # HELPERS
# # ---------------------
# def embed_text(text: str):
#     """Generate embeddings for a given text using OpenAI."""
#     response = client.embeddings.create(
#         model="text-embedding-3-small",  # or "text-embedding-3-large"
#         input=text,
#     )
#     return response.data[0].embedding


# def create_vectorstore(text: str, namespace: str = NAMESPACE):
#     """Split text into chunks, create embeddings, and upsert into Pinecone."""
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = splitter.split_text(text)

#     vectors = []
#     for chunk in chunks:
#         # Create stable deterministic ID for deduplication
#         chunk_id = hashlib.md5(chunk.encode("utf-8")).hexdigest()
#         embedding = embed_text(chunk)

#         recored = ({"id": chunk_id, "metadata": {"text": chunk}}, embedding)

#     if vectors:
#         index.upsert(vectors=vectors, namespace=namespace)


# def query_vectorstore(query: str, namespace: str = NAMESPACE, top_k: int = 3):
#     """Query Pinecone for most relevant chunks given a user query."""
#     query_embedding = embed_text(query)

#     results = index.query(
#         vector=query_embedding, top_k=top_k, include_metadata=True, namespace=namespace
#     )
#     return results


# # ---------------------
# # STREAMLIT UI
# # ---------------------
# st.title("📄 PDF Q&A with Pinecone + OpenAI (RAG)")

# uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# if uploaded_file is not None:
#     pdf = PdfReader(uploaded_file)
#     text = ""
#     for page in pdf.pages:
#         if page.extract_text():
#             text += page.extract_text()

#     if st.button("Process PDF"):
#         with st.spinner("Processing and storing PDF in Pinecone..."):
#             create_vectorstore(text)
#         st.success("✅ PDF embedded and stored in Pinecone!")

# query = st.text_input("🔍 Ask a question about the document:")

# if query:
#     results = query_vectorstore(query)

#     st.subheader("🔎 Retrieved Context:")
#     for match in results.matches:
#         st.write(match.metadata["text"])

#     # Construct final prompt for OpenAI
#     context = " ".join([m.metadata["text"] for m in results.matches])
#     prompt = f"Answer the question based only on the following context:\n\n{context}\n\nQuestion: {query}\nAnswer:"

#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant that only answers using the given context.",
#             },
#             {"role": "user", "content": prompt},
#         ],
#     )

#     st.subheader("💡 Answer:")
#     st.write(completion.choices[0].message.content)


from ai_agents.demo import simple_agent


t = simple_agent("What is 25 squared?")
print(t)
