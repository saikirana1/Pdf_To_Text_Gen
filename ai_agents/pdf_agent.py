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
main_agent_model=os.getenv("main_agent_model")
child_agent_model=os.getenv("openai_model")

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
            """
            You are a Retrieval-Augmented Generation (RAG) assistant.
            Your primary task is to answer user questions using the function tool named `query_pdf`.
            ### MANDATORY RULES:
            1. You must ALWAYS call the tool `query_pdf` before giving any answer.
            2. Pass the user's question exactly as received into the tool.
            3. Wait for the tool response and carefully analyze its metadata or text.
            4. Generate your final answer **only** using the data returned by the tool.
            5. If the tool returns no relevant results, reply exactly:
               "No related information found in the document."
            6. Never guess, assume, or use your own knowledge.
            7. Do not skip the tool call under any condition.
            """
        ),
        tools=[query_pdf],
        handoff_description=(
            "When a user asks any question, first use the `query_pdf` tool to fetch data "
            "from the document, then respond using the information from that tool only."
        ),
        model_settings=ModelSettings(tool_choice="required"),
        tool_use_behavior="run_llm_again",
        model=child_agent_model,
    )
    casual_agent=Agent(
        
         name="CASUAL_AGENT",
        instructions=(
            """
            You are a casual agent. 
            If the user says 'hi', 'hello', or 'how are you', respond politely.
            For any other type of query, do not respond and let other agents handle it.
            """
        ),
        tools=[query_pdf],
        handoff_description=(
            """When a user asks any question, related hi, how are you  then simple respond """
        ),
       
        model=child_agent_model,
        
        
        
    )
    allocator_agent = Agent(
        name="Allocator",
        instructions=(
           "You are a routing agent. Forward simple greetings to CASUAL_AGENT "
            "and all other questions to RAG_AGENT."
        ),
        handoffs=[rag_agent,casual_agent],
        model=main_agent_model,
    )
    print("Tools available:", rag_agent.tools)
    result = Runner.run_streamed(allocator_agent, input_prompt, session=session)
    print("Active Agent:", result.last_agent.name)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            yield event.data.delta
        else:
            pass
