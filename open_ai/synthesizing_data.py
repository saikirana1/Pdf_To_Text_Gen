from agents import Runner
import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, SQLiteSession
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv()
 
session = SQLiteSession("simple@gmail.com", "conversation_history.db")
async def synthesizing_data(question, sql_command, final_result):
    print(question)
    print(sql_command)
    print(final_result, "--------------->")
    synthesize_data = Agent(
        name="Synthesize Data",
        handoff_description="""
            synthesize the data i will give the user quation , sql query and sql result 
            for this generate the meaningful sentence 
           
            """,
        instructions=""" 
        synthesize the data i will give the user quation, sql query and sql
        """,
    )

    allocator_agent = Agent(
        name="Allocator Agent",
        instructions="Run the Agent for the Synthesizing data",
        handoffs=[synthesize_data],
    )

    result = Runner.run_streamed(
        allocator_agent,
        f"""This is the user quation{question} , This is the sql query {sql_command} and This is the Query result {final_result}
       Generate a meaningful, easy-to-understand sentence based on this data.
        """,
        session=session,
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # print("se",event.data.delta)
            print(event.data.delta, end="", flush=True)
            # print(event.data)
            yield event.data.delta
        else: 
            pass
        