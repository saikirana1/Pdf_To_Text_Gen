from pydantic import BaseModel
from agents import Runner, Agent
from dotenv import load_dotenv
from openai import OpenAI
from data_model.data_decison_agent import DataDecision
import asyncio

load_dotenv()


class Result(BaseModel):
    answer: str


async def data_decison_agent(input_prompt: str):
    bank_agent = Agent(
        name="BANK_DATA_AGENT",
        model="gpt-4o-mini",
        instructions="""
        You are an expert at identifying data related to transactions,
        including debit and credit details.
        """,
        output_type=Result,
        handoff_description="""
        Use this agent if the data is related to transaction details 
        such as debit and credit operations.
        """,
    )
    invoice_agent = Agent(
        name="INVOICE_AGENT",
        model="gpt-4o-mini",
        instructions="""
        You are an expert at identifying invoice-related data,
        including invoice IDs and item/product details.
        """,
        output_type=Result,
        handoff_description="""
        Use this agent if the data contains invoice ID, invoice date,
        CGST, SGST, product quantity, MRP price, Unit price, 
        HSN Code, and total amount.
        """,
    )
    normal_data_agent = Agent(
        name="NORMAL_DATA_AGENT",
        model="gpt-4o-mini",
        instructions="""
        You are an expert at identifying and extracting structured and semi-structured information 
    from documents. This includes:
    - Banking transaction forms (loans, financing)
    - Investment and risk assessment questionnaires
    - General document information (names, dates, IDs, amounts, financial terms)
    -  paragraphs, and key details
    Your task is to parse the document, identify the type of data, and extract key details accurately.
        """,
        output_type=Result,
        handoff_description="""
      Use this agent for any document that contains structured, semi-structured, 
    or general financial/administrative information. It can handle transaction forms, 
    investment profiles, questionnaires, and general paragraphs. 
    
        """,
        tool_use_behavior="stop_on_first_tool",
    )
    allocator_agent = Agent(
        model="gpt-4o-mini",
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[bank_agent, invoice_agent, normal_data_agent],
    )
    result = await Runner.run(allocator_agent, input_prompt)

    print("Active Agent:", result.last_agent.name)
    if result.last_agent.name == "BANK_DATA_AGENT":
        return DataDecision(agent="BANK_DATA_AGENT")
    elif result.last_agent.name == "INVOICE_AGENT":
        return DataDecision(agent="INVOICE_AGENT")
    else:
        return DataDecision(agent="NORMAL_DATA_AGENT")
