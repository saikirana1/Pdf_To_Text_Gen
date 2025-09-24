from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from ..pinecone_v_db.get_db_table import get_db_table
from ..pinecone_v_db.pinecone_api_client import pinecone_cli
from ..database_sql.query_data import query_data
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from .run_invoice_sql_agnet import run_rag_agent
from ..data_model.invoice_data_agent import InvoiceAgent
load_dotenv()


@function_tool
def query_name(text: str) -> dict:
    
    try:
        db, table = get_db_table()
        table="ice_cream_name"
        pc = pinecone_cli()
        index = pc.Index(db)
        results = index.search(
            namespace=table, query={"inputs": {"text": text}, "top_k": 1}
        )
        # print(results)
        name = results["result"]["hits"][0]["fields"]["description"]
        # print(results["result"]["hits"][0])
        print("i am from rag--name")
        print("name",name)
    except (KeyError, IndexError):
        name = "No results found for this one"
    return name


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def invoice_data_agent(input_prompt):
    sql_agent = Agent(
        name="SQL_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert at writing SQL queries for PostgreSQL database with the following schema:
           CREATE TABLE invoice (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_no VARCHAR UNIQUE,
    invoice_date DATE,
    CONSTRAINT uq_invoice_no UNIQUE (invoice_no)
);

CREATE TABLE item (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_no VARCHAR REFERENCES invoice(invoice_no) ON DELETE CASCADE,
    item_name VARCHAR,
    quantity FLOAT,
    unit_price FLOAT,
    unit_taxable_amount FLOAT,
    tax VARCHAR,
    unit_tax_amount FLOAT,
    amount FLOAT,
    mrp_price FLOAT,
    gst_number VARCHAR,
    CONSTRAINT fk_item_invoice FOREIGN KEY (invoice_no)
        REFERENCES invoice(invoice_no)
);
          For a given input, write an simple and accurate PostgreSQL query to run against the database.""",
        output_type=Query,
        handoff_description="""When users  asks for invoice related aggregates ,mathematical and if quations contains quantity,
        unit_price, unit_taxable_amount,tax,unit_tax_amount,amount,mrp_price and gst_number then use this agent
        """,
    )
    rag_agent = Agent(
        name="RAG_AGENT",
        model='gpt-4o-mini',
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question that related to the ice cream name such as Tub Strawberry , Lolly Strawberryor product name then run the tools
        Do not answer directly. Always run the tool and return its output as the answer.
        if quation on the item name and invoice_id  then use this other wise you leave it."""
        ),
        tools=[query_name],
        output_type=Result,
        handoff_description="""When users asks quation related to ice cream name and product name  such as Tub Strawberry , Lolly Strawberryor then run the tool
         if quation contains the product name and invoice_id then use tool call """,
        model_settings=ModelSettings(tool_choice="query_name"),
        tool_use_behavior="stop_on_first_tool",
    )

    allocator_agent = Agent(
        model='gpt-4o-mini',
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[sql_agent,rag_agent],
    )

    result = await Runner.run(allocator_agent, input_prompt)

    print("Active Agent:", result.last_agent.name)
    if result.last_agent.name == "SQL_AGENT":
        query_result = query_data(result.final_output.query)
        # print(query_result)
        return InvoiceAgent(agent=result.last_agent.name,sql_result=str(query_result), sql_query=result.final_output.query)
    elif result.last_agent.name == "RAG_AGENT":
        print("result.final_output",result.final_output)
        return await run_rag_agent(input_prompt,result.final_output)
        # print("i am rag ",result.final_output)

    return "None , your asking quations out of the subject"



