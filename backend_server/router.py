from fastapi import APIRouter, UploadFile, File, Form, Query, BackgroundTasks
import base64
from pydantic import BaseModel
from sqlmodel import select
from ..data_model.main_agent import MainAgent,DocumentAGENT,InvoiceAgent
import uuid

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from ..ai_agents.main_agent import main_agent
from fastapi.responses import StreamingResponse
from .event_generator import event_generator,event_generator_pdf
from ..open_ai.synthesizing_data import synthesizing_data
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


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
                 if main_agent_data.get("child_agent")=="SQL_AGENT":
                     return StreamingResponse(event_generator(user_question, main_agent_data.get("sql_query"), main_agent_data.get("sql_result")), media_type="text/event-stream")
                 elif main_agent_data.get("child_agent")=="RAG_AGENT":
                     return StreamingResponse(event_generator(user_question, main_agent_data.get("sql_query"), main_agent_data.get("sql_result")), media_type="text/event-stream")
            if parent_agent=="DOCUMENT_AGENT":
                 print("i am document from the parent")
                 print("i am from rag router pdf")
                 return StreamingResponse(event_generator_pdf(user_question), media_type="text/event-stream")
            else:
                 print("nothing to match")

            
                 
                    
                  
             