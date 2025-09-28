from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from database_sql.query_data import query_data
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from data_model.run_rag_sql_model import SqlRagaent
load_dotenv()

class Result(BaseModel):
    answer: str


class Query(BaseModel):
    query: str


async def run_rag_agent(quation,answer):
    sql_agent = Agent(
        model='gpt-4o-mini',
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
          For a given input, write an simple and accurate PostgreSQL query to run against the database.
          if the {answer } is like  no transaction information available,not found and none then use this SQL_AGENT
          
          """,
        output_type=Query,
        handoff_description=f"""
                 based on this quation {quation} write the sql query on this {answer}
                 most of the time this will use finally write the query on description.
                   
        """,
    )
    continue_process=Agent(
        model='gpt-4o-mini',
        name="Continue_AGENT",
        instructions=""" in this sentance is like There are no recent transactions available for STARCHIK FOODS PRIVATE LIMITED.,
              not found and no data then don't run this use the SQL_AGENT """,
        output_type=Query,
        handoff_description=f"if this answer is like {answer} no date transaction found like that . don't use it Otherwise, use it",
    )
    

    allocator_agent = Agent(
        model='gpt-4o-mini',
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[sql_agent,continue_process],
    )

    result = await Runner.run(allocator_agent, quation)

    print("Active Agent:", result.last_agent.name)
    if result.last_agent.name == "SQL_AGENT":
        print("from rag sql",result.final_output.query)
        query_result = query_data(result.final_output.query)
        print("query_result",query_result)
        # print(query_result)
        return SqlRagaent(agent=result.last_agent.name,sql_query=result.final_output.query,sql_result=str(query_result[0]))
    if result.last_agent.name == "Continue_AGENT":
        print(result)
        return result.last_agent.name,result.final_output.query
