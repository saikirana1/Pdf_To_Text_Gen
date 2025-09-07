# class MathAnswer(BaseModel):
#     question: str
#     answer: int
#     reasoning: str


# @function_tool
# def solve_addition(a: int, b: int):
#     print("sdafkh")
#     return a + b


# class Query(BaseModel):
#     query: str


# class Answer(BaseModel):
#     answer: str


# @function_tool
# def solve_addition(a: int, b: int) -> dict:  # return dict
#     return {
#         "question": f"{a} + {b}",
#         "answer": a + b,
#         "reasoning": f"Adding {a} and {b} gives {a + b}.",
#     }


# def multi_agent_handoff():
#     sql_agent = Agent(
#         name="SQL_AGENT",
#         instructions="""You are an expert at writing SQL queries for PostgreSQL database with the following schema:

#             CREATE TABLE transaction (
#                 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
#                 transaction_id VARCHAR(255),
#                 transaction_date DATE,
#                 withdrawal NUMERIC,
#                 deposit NUMERIC,
#                 balance NUMERIC,
#                 description TEXT
#             );

#             For a given input, write an simple and accurate PostgreSQL query to run against the database.""",
#         output_type=Query,
#     )
#     # rag_agent = Agent(
#     #     name="""You do the similarity search on userQuery if the quation
#     #           not belongs to the sql query then do the similarity search using the tool calling
#     #           like you will do the product name comes then do it

#     #     """,
#     #     instructions="DO the Mathematical operations",
#     #     output_type=Answer,
#     #     tools=[filter_records],
#     # )
#     agent = Agent(
#         name="MathAgent",
#         instructions="Use the tool to solve addition problems.",
#         tools=[solve_addition],
#         output_type=MathAnswer,
#     )
#     allocator_agent = Agent(
#         name="Allocator",
#         instructions="Decide which agent to forward the question to based on its topic.",
#         handoffs=[sql_agent, agent],
#     )

#     query1 = "what is the my  total  withdrawal amount "
#     query2 = "what is 6+9"

#     result1 = Runner.run_sync(allocator_agent, query1)
#     result2 = Runner.run_sync(allocator_agent, query2)

#     print(result1.final_output)
#     print(result2.final_output)
#     return

import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Runner, Agent, function_tool

from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_client

load_dotenv()


@function_tool
def query_text(text: str):
    print("hi")
    db, table = get_db_table()
    pc = pinecone_client()
    index = pc.Index(db)

    results = index.search(
        namespace=table,
        query={"inputs": {"text": text}, "top_k": 1},
    )
    return results


class Result(BaseModel):
    answer: dict  # store Pinecone response as a dict


class Query(BaseModel):
    query: str


def multi_agent_handoff():
    sql_agent = Agent(
        name="SQL_AGENT",
        instructions="""Write an SQL query for PostgreSQL transaction table.""",
        output_type=Query,
    )

    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=" always exiguites if not sql then run function_tool If the query is about semantic search (not SQL), use the tool to search Pinecone and return results.",
        tools=[query_text],
        output_type=Result,
    )

    allocator_agent = Agent(
        name="Allocator",
        instructions="Forward queries to the right agent based on topic.",
        handoffs=[sql_agent, rag_agent],
    )

    query1 = "What is my total withdrawal amount?"
    query2 = "STARCHIK FOODS PRIVATE LIMIT"

    result1 = Runner.run_sync(allocator_agent, query1)
    result2 = Runner.run_sync(allocator_agent, query2)

    print("SQL Agent output:", result1.final_output)
    print("RAG Agent output:", result2.final_output)
