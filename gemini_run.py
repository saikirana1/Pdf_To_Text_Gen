from google import genai
import os 
from dotenv import load_dotenv
load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.

from google.genai import types
import io
import httpx

client = genai.Client()

long_context_pdf_path="https://yazfblhnovanrbxelnmb.supabase.co/storage/v1/object/public/pdf/pdf_files/invoice-with-gst-19714.pdf"

# Retrieve and upload the PDF using the File API
doc_io = io.BytesIO(httpx.get(long_context_pdf_path).content)

sample_doc = client.files.upload(
  # You can pass a path or a file-like object here
  file=doc_io,
  config=dict(
    mime_type='application/pdf')
)
while True:
    prompt=input("Enter the input")
    if input =="no":
        break
    response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=[sample_doc, prompt],
   
    )
    for chunk in response:
      print(chunk.text,end="")




# response = client.models.generate_content_stream(
#     model="gemini-2.5-flash",
#     contents=["Explain how AI works"]
# )
# for chunk in response:
#     print(chunk.text, end="",flush=True)