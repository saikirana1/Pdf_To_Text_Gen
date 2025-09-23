from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from .invoice_data_agent import invoice_data_agent
from .pdf_agent import pdf_agent

from .multi_agent_handoff import multi_agent_handoff
from ..open_ai.synthesizing_data import synthesizing_data
from typing import Optional,List,Tuple
from ..data_model.main_agent import DocumentAGENT,BankAgent,InvoiceAgent,ReturnData
load_dotenv()


class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def main_agent(input_prompt):
    agents={"parent_agent":"","child_agent":""}
    bank_agent = Agent(
        name="Bank_Agent",
        model='gpt-4o-mini',
        instructions="""You are an expert in identifying questions related to bank transactions and bank-related queries.""",
        output_type=Query,
        handoff_description="""Use this agent if the question involves bank transactions or bank statement related queries."""
    )

    invoice_agent = Agent(
        name="Invoice_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert in identifying questions related to invoice data or queries related to invoice data.""",
        output_type=Result,
        handoff_description="""Use this agent if the question involves invoice ID or products; if query contains 'invoice', use this one."""
    )

    document_agent = Agent(
        name="Document_AGENT",
        model='gpt-4o-mini',
        instructions="""You are an expert in identifying questions related to documents or text-based queries.""",
        output_type=Result,
        handoff_description="""Use this agent if the question involves documents or specific text-based queries, such as those using RAG (Retrieval-Augmented Generation)."""
    )


    allocator_agent = Agent(
        model='gpt-4o-mini',
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[bank_agent, invoice_agent,document_agent],
    )

    result = await Runner.run(allocator_agent, input_prompt)

    print("Active Agent:", result.last_agent.name)
    if result.last_agent.name == "Bank_Agent":
        agent_type,query_result,sql_query = await multi_agent_handoff(input_prompt)
        # agents["child_agent"]=agent_type
        # agents["parent_agent"]=result.last_agent.name
        
        #final_syth_data = await synthesizing_data(input_prompt,query_result[1],query_result[0][0])
        # print(result)
        # print(query_result)
        # print("this is query_result",query_result[0][0])
        # print("this is sql query",query_result[1],type(query_result[1]))

        # print(type(query_result[0]))
        # query_result = query_data(query_result)
        print("i am from bank")
        # print(query_result)
        # print(result.final_output.query)
        return BankAgent(child_agent==agent_type,sql_result=query_result,sql_query=sql_query)
    elif result.last_agent.name == "Invoice_AGENT":
        result=await invoice_data_agent(input_prompt)
        print(result)
        # t=run_rag_agent(input_prompt,result.final_output,result.final_output)
        # print("i am rag ",result.final_output)
        return result
    elif result.last_agent.name == "Document_AGENT":
        pdf_result=await pdf_agent(input_prompt)
        # print(result)
        return pdf_result
    else:
       resutl=pdf_agent(input_prompt)
    #    print(result)
    