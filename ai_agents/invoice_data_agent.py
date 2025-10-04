from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_cli
from database_sql.query_data import query_data
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from .run_invoice_sql_agnet import run_rag_agent
from data_model.invoice_data_agent import InvoiceAgent
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
        # print("results===========>", results)
        # # print(results)
        # name = results["result"]["hits"][0]["fields"]["description"]
        # # description = results["result"]["hits"][0]["fields"]["description"]
        # # print("i am from rag--name")
        # # print("name",name)
        # print(name, "=================================>")
    except Exception as e:
        print("i am error from the invoice rag agnet-=======------->", e)
        name = "No results found for this one"
    return results


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def invoice_data_agent(input_prompt):
    sql_agent = Agent(
        name="SQL_AGENT",
        model="gpt-4o-mini",
        instructions="""You are an expert at writing SQL queries for PostgreSQL database with the following schema:
           -- Table: invoice
CREATE TABLE invoice (
    invoice_no UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    invoice_date DATE,
    CONSTRAINT invoice_invoice_no_key UNIQUE(invoice_no)
);

-- Table: item
CREATE TABLE item (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_no UUID REFERENCES invoice(invoice_no) ON DELETE CASCADE,
    item_name TEXT,
    hsn_code TEXT,
    quantity NUMERIC,
    unit_price NUMERIC,
    unit_taxable_amount NUMERIC,
    tax TEXT,
    unit_tax_amount NUMERIC,
    amount NUMERIC,
    mrp_price NUMERIC
);

-- Table: bank_details
CREATE TABLE bank_details (
    invoice_no UUID REFERENCES invoice(invoice_no) ON DELETE CASCADE,
    account_number TEXT,
    ifsc_code TEXT,
    holder_name TEXT,
    bank_name TEXT,
    branch TEXT
);

-- Table: seller
CREATE TABLE seller (
    invoice_no UUID REFERENCES invoice(invoice_no) ON DELETE CASCADE,
    address TEXT,
    contact TEXT,
    gst_number TEXT,
    fssai_no TEXT,
    pin_code TEXT
);

-- Table: payment
CREATE TABLE payment (
  
    invoice_no UUID REFERENCES invoice(invoice_no) ON DELETE CASCADE,
    sub_total NUMERIC,
    s_gst NUMERIC,
    c_gst NUMERIC,
    discount NUMERIC,
    total NUMERIC
);

-- Table: customer
CREATE TABLE customer (
    invoice_no UUID REFERENCES invoice(invoice_no) ON DELETE CASCADE,
    name TEXT,
    address TEXT,
    gst_number TEXT
);

          For a given input, write an simple and accurate PostgreSQL query to run against the database.""",
        output_type=Query,
        handoff_description="""When users  asks for invoice related aggregates ,mathematical and if quations contains quantity,
        unit_price, unit_taxable_amount,tax,unit_tax_amount,amount,mrp_price and gst_number then use this agent
        """,
    )
    rag_agent = Agent(
        name="RAG_AGENT",
        model="gpt-4o-mini",
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question that related to the ice cream name such as Tub Strawberry , Lolly Strawberryor product name then run the tools
        Do not answer directly. Always run the tool and return its output as the answer.
        if quation on the item name and invoice_id  then use this other wise you leave it."""
        ),
        tools=[query_name],
        handoff_description="""When users asks quation related to ice cream name and product name  such as Tub Strawberry , Lolly Strawberryor then run the tool
         if quation contains the product name and invoice_id then use tool call """,
        model_settings=ModelSettings(tool_choice="query_name"),
        tool_use_behavior="run_llm_again",
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
        print("i am query", result.final_output.query)
        print("i am query_result", query_result)
        # print(query_result)
        return InvoiceAgent(agent=result.last_agent.name,sql_result=str(query_result), sql_query=result.final_output.query)
    elif result.last_agent.name == "RAG_AGENT":
        print("result.final_output rag_result==========>", result.final_output)
        # rag_result = await run_rag_agent(input_prompt, result.final_output)
        # print("rag_result===========================", rag_result)
        # ra_result = rag_result.model_dump()
        return InvoiceAgent(
            agent=result.last_agent.name, rag_result=result.final_output
        )
        # print("i am rag ",result.final_output)