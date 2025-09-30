from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from database_sql.query_data import query_data
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from data_model.invoice_data_agent import InvoiceAgent
load_dotenv()

class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def run_rag_agent(input_prompt,name):
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
        handoff_description="""Write sql_query on this exact name don't split and remove any thing from this use like  basically this is the 
           user quation based on this quation ,product name and sql schema write better sql query""",
    )
    # continue_process=Agent(
    #     model='gpt-4o-mini',
    #     name="Continue_AGENT",
    #     instructions=""" in this sentance is like There are no recent transactions available for STARCHIK FOODS PRIVATE LIMITED.,
    #           not found and no data then don't run this use the SQL_AGENT """,
    #     output_type=Query,
    #     handoff_description=f"if this answer is like {answer} no date transaction found like that . don't use it Otherwise, use it",
    # )
    

    allocator_agent = Agent(
        model='gpt-4o-mini',
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[sql_agent],
    )

    result = await Runner.run(allocator_agent, name)

    print("Active Agent: i am invoice", result.last_agent.name)
    query_result = ""
    if result.last_agent.name == "SQL_AGENT":
        # print("from rag sql",result.final_output.query)
        query_result = query_data(result.final_output.query)
        print("i am query", result.final_output.query)
        print("i am query_result", query_result)
        #print(query_data)
        # print("query_resultfdsfsf",query_result)
        # print(result.final_output.query,"result.final_output.query")
        return InvoiceAgent(agent=result.last_agent.name,sql_result=str(query_result[0]), sql_query=result.final_output.query)
