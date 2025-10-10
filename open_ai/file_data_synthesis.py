from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_cli

import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, SQLiteSession

from dotenv import load_dotenv
import os


load_dotenv()
session_db_name = os.getenv("session_db_name")
session_con_user = os.getenv("session_con_user")

session = SQLiteSession("session_con_user", "session_db_name1.db")


async def file_data_synthesis(input_question, urls):
    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=(
            """
            You are an agent responsible for generating accurate and concise answers
            based on the provided data and the user's question.
            Respond only in natural, sentence-based text suitable for React Markdown.
            DO NOT use pipes (||). 
            ;j
           """
        ),
        handoff_description="""
           Provide well-structured, natural-language responses.
           generate complete sentences compatible with React Markdown.
          DO NOT use pipes (||). 
        """,
        tool_use_behavior="run_llm_again",
        model="gpt-4o-mini",
    )
    allocator_agent = Agent(
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[rag_agent],
        model="gpt-4o-mini",
        tool_use_behavior="stop_on_first_tool",
    )
    file_inputs = [{"type": "input_file", "file_url": url} for url in urls]

    input_message = {
        "role": "user",
        "content": [
            {"type": "input_text", "text": f"User Question: {input_question}"},
            *file_inputs,
        ],
    }

    result = Runner.run_streamed(
        allocator_agent,
        input=[input_message],
    )

    print("Active Agent:", result.last_agent.name)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            yield event.data.delta
        else:
            pass
