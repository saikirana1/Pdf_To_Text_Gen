from fastapi import APIRouter, UploadFile, File, Form, Query, BackgroundTasks, Request
import json
import base64
from pydantic import BaseModel
from sqlmodel import select
from data_model.main_agent import MainAgent,DocumentAGENT,InvoiceAgent
import uuid
import asyncio
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from ai_agents.main_agent import main_agent
from fastapi.responses import StreamingResponse
from .event_generator import (
    event_generator,
    event_generator_pdf,
    event_generator_rag,
    event_generator_file,
)
from open_ai.synthesizing_data import synthesizing_data
from ai_agents.data_decison_agent import data_decison_agent
from clean_pdf_data.extract_pages import extract_pages
from clean_pdf_data.pdf_json_data import pdf_to_json
from clean_pdf_data.pdf_plain_text import extract_plain_text_outside_tables
from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract
import io
import os
from open_ai.invoice_pdf_to_json import invoice_pdf_json
from open_ai.create_pdf_embedings import create_pdf_embedings
from pinecone_v_db.insert_chunks import insert_chunks
from supabase_packages.upload_file import upload_file_to_supabase
from database_sql.insert_and_get_file_data import (
    insert_file_record,
    get_all_files_from_db,
)
from supabase_packages.upload_file import uplod_file_details_sql
from open_ai.client import openai_client
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
client = openai_client()
router = APIRouter()

@router.get("/get_response")
async def sse_endpoint(user_question: str):
            result : MainAgent= await main_agent(user_question)
            main_agent_data=result.model_dump()
            parent_agent=main_agent_data.get("parent_agent")
            print(parent_agent)
            if parent_agent=="BANK_AGENT":
              if main_agent_data.get("child_agent")=="SQL_AGENT":
                   return StreamingResponse(event_generator(user_question, main_agent_data.get("sql_query"), main_agent_data.get("sql_result")), media_type="text/event-stream")
              elif main_agent_data.get("child_agent")=="RAG_AGENT":
                   return StreamingResponse(event_generator(user_question, main_agent_data.get("sql_query"), main_agent_data.get("sql_result")), media_type="text/event-stream") 
            if parent_agent=="INVOICE_AGENT":
                if main_agent_data.get("child_agent") == "SQL_AGENT":
                    print(
                        user_question,
                        main_agent_data.get("sql_query"),
                        main_agent_data.get("sql_result"),
                        "===========>from router input",
                    )
                    return StreamingResponse(
                        event_generator(
                            user_question,
                            main_agent_data.get("sql_query"),
                            main_agent_data.get("sql_result"),
                        ),
                        media_type="text/event-stream",
                    )
                elif main_agent_data.get("child_agent") == "RAG_AGENT":
                    return StreamingResponse(
                        event_generator_rag(user_question),
                        media_type="text/event-stream",
                    )
            if parent_agent=="DOCUMENT_AGENT":
                 print("i am document from the parent")
                 print("i am from rag router pdf")
                 return StreamingResponse(event_generator_pdf(user_question), media_type="text/event-stream")
            else:
                 print("nothing to match")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        from io import BytesIO

        file_stream = BytesIO(contents)
        public_url = await upload_file_to_supabase(file.filename, file_stream)
        print(public_url)
        file_record = insert_file_record(
            file_name=file.filename,
            file_url=public_url,
            file_index="",
        )
        await file.seek(0)
        pdf_bytes = await file.read()
        filename = file.filename
        _, file_extension = os.path.splitext(filename)
        with open(f"demo{file_extension}", "wb") as f:
            f.write(pdf_bytes)
        print("file type is", file_extension)
        two_pages_data = extract_pages(f"demo{file_extension}")
        agent_result = await data_decison_agent(two_pages_data)
        agent = agent_result.model_dump().get("agent")
        print(type(agent))
        if agent == "BANK_DATA_AGENT":
            table_data = pdf_to_json(f"demo{file_extension}", skip_columns=None)
            plan_text = extract_plain_text_outside_tables(f"demo{file_extension}")
            result = pdf_to_json_data_extract(table_data, plan_text)
            print("extracted result is", result)

        elif agent == "INVOICE_AGENT":
            print("i am in invoice agent elif===========>")
            result = invoice_pdf_json(f"demo{file_extension}")
        elif agent == "NORMAL_DATA_AGENT":
            data = create_pdf_embedings(f"demo{file_extension}")
            result = insert_chunks(data)
            print("extracted result is", result)
        await asyncio.sleep(10)
        two_pages_data = {"message": "File processed successfully"}

    except Exception as e:
        return {"status": "error", "result": "sd"}
    return {
        "status": "success",
        "result": two_pages_data,
    }


@router.post("/upload_file")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        from io import BytesIO

        file_stream = BytesIO(contents)
        public_url = await upload_file_to_supabase(file.filename, file_stream)
        print(public_url)
        file_record = insert_file_record(
            file_name=file.filename,
            file_url=public_url,
            file_index="",
        )
        print(file_record)
        return {
            "url": public_url,
            "status": "success",
        }

    except Exception as e:
        return {"error": str(e), "status": "error"}


@router.get("/files")
def get_all_files():
    return get_all_files_from_db()


@router.get("/get_file_data")
async def get_responses(request: Request):
    user_question = request.query_params.get("user_question", "")
    urls_param = request.query_params.get("urls", "[]")
    file_urls = json.loads(urls_param)

    return StreamingResponse(
        event_generator_file(user_question, file_urls), media_type="text/event-stream"
    )