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

session = SQLiteSession(session_con_user, session_db_name)


@function_tool
def query_invoice(text: str) -> dict:
    try:
        db, table = get_db_table()
        table = "ice_cream_name"
        pc = pinecone_cli()
        index = pc.Index(db)
        results = index.search(
            namespace=table, query={"inputs": {"text": text}, "top_k": 1}
        )
        # print("results===========>", results)
        # # print(results)
        # name = results["result"]["hits"][0]["fields"]["description"]
        # # description = results["result"]["hits"][0]["fields"]["description"]
        # # print("i am from rag--name")
        # # print("name",name)
        # print(name, "=================================>")
    except Exception as e:
        print("i am error from the invoice rag agnet-=======------->", e)
        results = "No results found for this one"
    return results


async def invoice_rag_result(input_prompt):
    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question that related to the ice cream name such as Tub Strawberry , Lolly Strawberryor product name then run the tools
        products use this agent"""
        ),
        tools=[query_invoice],
        handoff_description="""
        When users asks quation related to ice cream name and product name  such as Tub Strawberry , Lolly Strawberryor then run the tool
        if quation contains the product name and invoice_id then use tool call
        products and dates related then use this agent
        """,
        model_settings=ModelSettings(tool_choice="query_invoice"),
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

    result = Runner.run_streamed(allocator_agent, input_prompt, session=session)

    print("Active Agent:", result.last_agent.name)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            yield event.data.delta
        else:
            pass
