from google import genai
import io
import httpx
import os 
from dotenv import load_dotenv
load_dotenv()


from google.genai import types
client = genai.Client()

def pdf_data_urls(prompt:str,urls:list):
  doc_urls_prompt=[]
  for url in urls:
     url_p= io.BytesIO(httpx.get(url).content)
     upload_dict = client.files.upload(
        file=url_p,
        config=dict(mime_type='application/pdf')
      )
     doc_urls_prompt.append(upload_dict)
  doc_urls_prompt.append(prompt)
  return doc_urls_prompt
    

async def file_data_response(prompt,urls):
      doc_urls_prompt=pdf_data_urls(prompt,urls)
      response = client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        
        contents= doc_urls_prompt)
      for chunk in response:
       print(chunk.text,end="",flush=True)
       yield chunk.text