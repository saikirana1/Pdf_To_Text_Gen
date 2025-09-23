from fastapi import APIRouter, UploadFile, File, Form, Query, BackgroundTasks
import base64
from pydantic import BaseModel
from sqlmodel import select

import uuid

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from ..ai_agents.main_agent import main_agent
from fastapi.responses import StreamingResponse

from ..open_ai.synthesizing_data import synthesizing_data
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


router = APIRouter()

@router.get("/get_response")
async def sse_endpoint(user_question: str):
            agents,query_result,sql_query= await main_agent(user_question)
            print(agent,"agent")
            print(user_prompt,"user_prompt")
            print(sql_query,"sql_query")
            print(query_output,"query_output")
            print(user_question,"user_question")
            if agents.get("parent_agent")=="Bank_Agent":
              
              if agents.get("child_agent")=="SQL_AGENT":
                 async def event_generator():
                    async for chunk in synthesizing_data(user_question, sql_query, query_result):
                #    print("R",chunk)
                     print(chunk, end="", flush=True)
                     yield f"data: {chunk}\n\n"  # SSE format for frontend EventSource

                 return StreamingResponse(event_generator(), media_type="text/event-stream")
             