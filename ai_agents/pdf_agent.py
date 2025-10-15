from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_cli
from pinecone_v_db.generate_embeddings import generate_embedding
import asyncio

from openai import OpenAI
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv
import os
from pinecone_v_db.get_db_table import dense_get_db_table

load_dotenv()
session_db_name = os.getenv("session_db_name")
session_con_user = os.getenv("session_con_user")

session = SQLiteSession(session_con_user, session_db_name)


@function_tool
def query_pdf(question: str) -> dict:
    print("====================> i am form tool call pdf data")
    try:
        pc = pinecone_cli()
        db, table_name = dense_get_db_table()
        index = pc.Index(db)
        vector = generate_embedding(question)
        response = index.query(
            vector=vector,
            namespace=table_name,
            top_k=1,
            include_metadata=True,
            include_values=False,
        )
        print("response---------------->", response)
        return {"results": response}
    except Exception as e:
        print("error from tool ---------->", e)
        return {"error": str(e)}


async def pdf_agent(input_prompt):
    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=(
            """you should run the tool call and 
            based on tool call data give response
            You Should run the function_tool
            """
        ),
        tools=[query_pdf],
        handoff_description="""
        based on tool call response give the better sentences
        any quation run this agent and also run the tool call 
        """,
        model_settings=ModelSettings(tool_choice="required"),
        tool_use_behavior="run_llm_again",
        model="gpt-4o-mini",
    )
    allocator_agent = Agent(
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[rag_agent],
        model="gpt-4o-mini",
    )

    result = Runner.run_streamed(allocator_agent, input_prompt)

    print("Active Agent:", result.last_agent.name)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            yield event.data.delta
        else:
            pass
