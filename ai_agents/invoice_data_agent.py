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


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def invoice_data_agent(input_prompt):
    sql_agent = Agent(
        name="SQL_AGENT",
        model="gpt-4o-mini",
        instructions="""You are an expert at writing SQL queries for a PostgreSQL database.
Below is the database schema:
you should use invoiced or any unique key then use in sql query do't put empty
-- Table: invoice
CREATE TABLE invoice (
invoice_no VARCHAR(255) UNIQUE NOT NULL,
invoice_date DATE
);

-- Table: item
CREATE TABLE item (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
invoice_no VARCHAR(255) REFERENCES invoice(invoice_no) ON DELETE CASCADE,
item_name VARCHAR(255),
hsn_code VARCHAR(255),
quantity NUMERIC,
unit_price NUMERIC,
unit_taxable_amount NUMERIC,
tax VARCHAR(255),
unit_tax_amount NUMERIC,
amount NUMERIC,
mrp_price NUMERIC
);

-- Table: bank_details
CREATE TABLE bank_details (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
invoice_no VARCHAR(255) REFERENCES invoice(invoice_no) ON DELETE CASCADE,
account_number VARCHAR(255),
ifsc_code VARCHAR(255),
holder_name VARCHAR(255),
bank_name VARCHAR(255),
branch VARCHAR(255)
);

-- Table: seller
CREATE TABLE seller (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
invoice_no VARCHAR(255) REFERENCES invoice(invoice_no) ON DELETE CASCADE,
address VARCHAR(255),
contact VARCHAR(255),
gst_number VARCHAR(255),
fssai_no VARCHAR(255),
pin_code VARCHAR(255)
);

-- Table: payment
CREATE TABLE payment (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
invoice_no VARCHAR(255) REFERENCES invoice(invoice_no) ON DELETE CASCADE,
sub_total NUMERIC,
s_gst NUMERIC,
c_gst NUMERIC,
discount NUMERIC,
total NUMERIC
);

-- Table: customer
CREATE TABLE customer (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
invoice_no VARCHAR(255) REFERENCES invoice(invoice_no) ON DELETE CASCADE,
name VARCHAR(255),
address VARCHAR(255),
gst_number VARCHAR(255)
);

Your task:
- Write a **simple, valid, and accurate PostgreSQL query** based on the user’s question.
- Do **not** add explanations — just return the query.
- Prefer aggregate or mathematical operations (e.g., SUM, AVG, COUNT) when the question implies them.
- Always use correct table and column names from the schema.
If the user provides an invoice ID, use it in the query.
Rules:
While writing the query if user give the invoice number or id the use it
""",
        output_type=Query,
        handoff_description="""
Use this agent when the user asks for:
- Invoice-related **aggregates**, **mathematical operations**, or **calculations**.
- Questions involving fields like `quantity`, `unit_price`, `unit_taxable_amount`, `tax`, `unit_tax_amount`, `amount`, `mrp_price`, or `gst_number`.
Rules:
While writing the query if user give the invoice id the use it 
you should use invoiced or any unique key then use in sql query do't put empty
""",
    )

    rag_agent = Agent(
        name="RAG_AGENT",
        model="gpt-4o-mini",
        instructions=(
            """
You are a retrieval agent.
Use external data retrieval tools (RAG) when the question involves **product names** or **ice cream names**.

Examples:
- "Find the invoice that contains Tub Strawberry."
- "Show me all products named Lolly Strawberry."
- "Get details for the product Chocolate Cone in invoice XYZ."

Rules:
- Do NOT generate SQL.
- Always call the retrieval tool when the query mentions **item names** or **invoice IDs**.
- If the question does not include product names or invoice numbers, ignore it and let another agent handle it.
you user asking about single invoice number details then use it 
"""
        ),
        handoff_description="""
        you should use the this if the quation related to one invoice number 
Use this agent when the user’s question involves:
- Product names such as **Tub Strawberry**, **Lolly Strawberry**, etc.
- Any query that includes both an **item name** and **invoice_id**.
- Or when the user asks for a **summary or details** of an invoice.
Rules:
While writing the query if user give the invoice id the use it
you should use the user asking about single invoice number details then use it 
""",
        tool_use_behavior="stop_on_first_tool",
    )

    allocator_agent = Agent(
        model="gpt-4o-mini",
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[sql_agent, rag_agent],
    )

    result = await Runner.run(allocator_agent, input_prompt)

    print("Active Agent:", result.last_agent.name)

    if result.last_agent.name == "SQL_AGENT":
        query_result = query_data(result.final_output.query)
        print("i am query", result.final_output.query)
        print("i am query_result", query_result)
        # print(query_result)
        return InvoiceAgent(
            agent=result.last_agent.name,
            sql_result=str(query_result),
            sql_query=result.final_output.query,
        )

    elif result.last_agent.name == "RAG_AGENT":
        print("result.final_output rag_result==========>", result.final_output)
        # rag_result = await run_rag_agent(input_prompt, result.final_output)
        # print("rag_result===========================", rag_result)
        # ra_result = rag_result.model_dump()
        return InvoiceAgent(agent=result.last_agent.name)
        # print("i am rag ",result.final_output)
