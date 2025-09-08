import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
import json
from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_client
from database_sql.query_data import query_data
import asyncio

load_dotenv()


@function_tool
def query_text(text: str) -> dict:
    try:
        db, table = get_db_table()
        pc = pinecone_client()
        index = pc.Index(db)
        results = index.search(
            namespace=table, query={"inputs": {"text": text}, "top_k": 1}
        )
        print(results)
        description = results["result"]["hits"][0]["fields"]["description"]
    except (KeyError, IndexError):
        description = "No results found for this one"
    print(description)
    return description


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


def multi_agent_handoff(input_prompt):
    sql_agent = Agent(
        name="SQL_AGENT",
        instructions="""You are an expert at writing SQL queries for PostgreSQL database with the following schema:
           CREATE TABLE transaction (   
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                transaction_id VARCHAR(255),
                transaction_date DATE,             
                withdrawal NUMERIC,
                deposit NUMERIC,              
                balance NUMERIC,
                description TEXT
            );
          For a given input, write an simple and accurate PostgreSQL query to run against the database.""",
        output_type=Query,
        handoff_description="When users gives asks for transaction related aggregates ,mathematical quation and time related quation",
    )

    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question that contains or refers to a  description of transaction  
        (e.g. NEFT, RTGS, cheque, IMPS, UTR numbers, company names in descriptions), 
        you MUST call the tool `query_text` with the user's text. 
        Do not answer directly. Always run the tool and return its output as the answer."""
        ),
        tools=[query_text],
        output_type=Result,
        handoff_description="""When users gives a  description of transaction, use this agent to find similar description of transaction
            and  pass the user input to this tools """,
        model_settings=ModelSettings(tool_choice="query_text"),
        tool_use_behavior="stop_on_first_tool",
    )

    allocator_agent = Agent(
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[sql_agent, rag_agent],
    )
    # re = Runner.run_sync(allocator_agent, input=input_prompt)
    re = asyncio.run(Runner.run(allocator_agent, input_prompt))

    print("Active Agent:", re.last_agent.name)
    query_result = ""
    sql_query = ""
    if re.last_agent.name == "SQL_AGENT":
        query_result = query_data(re.final_output.query)
        print(query_result)
        return query_result, re.final_output.query
    elif re.last_agent.name == "RAG_AGENT":
        print(re.final_output)
        return re.final_output, sql_query
    return "None your asking quations out of the subject"
