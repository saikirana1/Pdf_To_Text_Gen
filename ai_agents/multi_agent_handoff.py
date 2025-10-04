from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_cli
from database_sql.query_data import query_data
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from .run_rag_sql_agent import run_rag_agent
from data_model.multi_agent_handoff import SqlRagaent

load_dotenv()


@function_tool
def query_text(text: str) -> dict:
    
    try:
        db, table = get_db_table()
        pc = pinecone_cli()
        index = pc.Index(db)
        results = index.search(
            namespace=table, query={"inputs": {"text": text}, "top_k": 1}
        )
        # print(results)
        description = results["result"]["hits"][0]["fields"]["description"]
        # print(results["result"]["hits"][0])
    except (KeyError, IndexError):
        description = "No results found for this one"
    return description


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def multi_agent_handoff(input_prompt):
    sql_agent = Agent(
        name="SQL_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert at writing SQL queries for PostgreSQL database with the following schema:
           CREATE TABLE account (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_number UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    ifsc_code TEXT,
    name TEXT
);

  CREATE TABLE transaction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id TEXT,
    transaction_date DATE,
    withdrawal DOUBLE PRECISION,
    deposit DOUBLE PRECISION,
    balance DOUBLE PRECISION,
    description TEXT,
    check_number TEXT,
    account_number UUID NOT NULL,
    CONSTRAINT fk_transaction_account FOREIGN KEY (account_number) 
        REFERENCES account(account_number)
);
          For a given input, write an simple and accurate PostgreSQL query to run against the database.""",
        output_type=Query,
        handoff_description="""When users  asks for bank transaction related aggregates ,mathematical quation and time related quation
        which means quation related to sql query then use this""",
    )

    rag_agent = Agent(
        name="RAG_AGENT",
        model='gpt-4o-mini',
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question that contains or refers to a  description of transaction  
        (e.g. NEFT, RTGS, cheque, IMPS, UTR numbers,human names ,company names in descriptions), 
        you MUST call the tool `query_text` with the user's text. 
        Do not answer directly. Always run the tool and return its output as the answer."""
        ),
        tools=[query_text],
        output_type=Result,
        handoff_description="""Use this agent when the user provides a transaction description 
or mentions names/company names to find similar transactions""",
        model_settings=ModelSettings(tool_choice="query_text"),
        tool_use_behavior="stop_on_first_tool",
    )

   

    allocator_agent = Agent(
        model='gpt-4o-mini',
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[sql_agent, rag_agent],
    )

    result = await Runner.run(allocator_agent, input_prompt)

    print("Active Agent:", result.last_agent.name)
    if result.last_agent.name == "SQL_AGENT":
        query_result = query_data(result.final_output.query)
        # print("query_result",query_result,type(query_result))
        # print(type(query_result))

        print("result.final_output.query--------->", result.final_output.query)
        print("query_result-------->", query_result)
        # print(query_result)
        #print(result.final_output.query)
        return SqlRagaent(agent=result.last_agent.name,sql_result=query_result, sql_query=result.final_output.query)
    elif result.last_agent.name == "RAG_AGENT":
        rag_result= await run_rag_agent(input_prompt,result.final_output)
        ra_result=rag_result.model_dump()

       
        # print("i am rag ",result.final_output)
        return SqlRagaent(agent=ra_result.get("agent"),sql_result=ra_result.get("sql_result"), sql_query=ra_result.get("sql_query"))
