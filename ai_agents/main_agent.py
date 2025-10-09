from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings, SQLiteSession
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from .invoice_data_agent import invoice_data_agent
from .pdf_agent import pdf_agent

from .multi_agent_handoff import multi_agent_handoff
from open_ai.synthesizing_data import synthesizing_data
from typing import Optional,List,Tuple
from data_model.main_agent import DocumentAGENT,InvoiceAgent,ReturnData,MainAgent
from dotenv import load_dotenv
import os


load_dotenv()
session_db_name = os.getenv("session_db_name")
session_con_user = os.getenv("session_con_user")

session = SQLiteSession(session_con_user, session_db_name)


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def main_agent(input_prompt)->ReturnData:
    bank_agent = Agent(
        name="BANK_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert in identifying questions related to bank transactions and bank-related queries.""",
        output_type=Query,
        handoff_description="""Use this agent if the question involves bank transactions or bank statement related queries."""
    )

    invoice_agent = Agent(
        name="INVOICE_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert in identifying questions related to invoice data or queries related to invoice data.""",
        output_type=Result,
        handoff_description="""Use this agent if the question involves invoice ID or products; if query contains 'invoice', use this one."""
    )

    document_agent = Agent(
        name="DOCUMENT_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert in identifying questions related to documents or text-based queries. such as 
        any topic related to with out structured data """,
        output_type=Result,
        handoff_description="""Use this agent if the question involves documents or specific text-based queries, such as those using RAG (Retrieval-Augmented Generation).
        with out structured data which relates to non tabular data then use this agent"""
    )


    allocator_agent = Agent(
        model='gpt-4o-mini',
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[bank_agent, invoice_agent,document_agent],
    )

    result = await Runner.run(allocator_agent, input_prompt, session=session)

    print("Active Agent:", result.last_agent.name)
    if result.last_agent.name == "BANK_AGENT":
        bank_account_result = await multi_agent_handoff(input_prompt)
        print("bank_account_result=====================>", bank_account_result)
        sql_agent=bank_account_result.model_dump()
        if sql_agent.get("agent")=="SQL_AGENT":
            print("i am from bank",sql_agent)
            return MainAgent(child_agent=sql_agent.get("agent"),parent_agent=result.last_agent.name,sql_result=sql_agent.get("sql_result"),sql_query=sql_agent.get("sql_query"))
        elif sql_agent.get("agent")=="RAG_AGENT":
            return MainAgent(child_agent=sql_agent.get("agent"),parent_agent=result.last_agent.name,sql_result=sql_agent.get("sql_result"),sql_query=sql_agent.get("sql_query"))
    
    elif result.last_agent.name == "INVOICE_AGENT":
        invoice_result = await invoice_data_agent(input_prompt)
        print("invoice_result============>", invoice_result)
        sql_agent=invoice_result.model_dump()
        if sql_agent.get("agent")=="SQL_AGENT":
            print("i am from invoice",sql_agent)
            return MainAgent(child_agent=sql_agent.get("agent"),parent_agent=result.last_agent.name,sql_result=sql_agent.get("sql_result"),sql_query=sql_agent.get("sql_query"))
        elif sql_agent.get("agent")=="RAG_AGENT":
            return MainAgent(
                child_agent=sql_agent.get("agent"),
                parent_agent=result.last_agent.name,
            )
    elif result.last_agent.name == "DOCUMENT_AGENT":
        # pdf_result=await pdf_agent(input_prompt)
        return MainAgent(child_agent="RAG_AGENT",parent_agent=result.last_agent.name)
    else:
       print("i am else")
       return MainAgent(child_agent="RAG_AGENT",parent_agent="DOCUMENT_AGENT")
    