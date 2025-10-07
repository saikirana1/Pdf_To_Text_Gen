from agents import Runner
import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, SQLiteSession
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv()
 
session = SQLiteSession("user_123")
async def synthesizing_data(question, sql_command, final_result):
    synthesize_data = Agent(
        name="Synthesize Data",
        handoff_description=f"""
        Specialist agent for synthesizing data.
        This is the user question: {question},
        this is the SQL command: {sql_command},
        and this is the final result: {final_result}.
        Generate the best sentence that the user will understand.
        don't use any currency symbol
        """,
        instructions="You provide help as a specialist agent for synthesizing data.",
    )

    allocator_agent = Agent(
        name="Allocator Agent",
        instructions="Run the Agent for the Synthesizing data",
        handoffs=[synthesize_data],
    )

    result = Runner.run_streamed(
        allocator_agent,
        "Generate the best sentence that the user will understand.",
        session=session,
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # print("se",event.data.delta)
            # print(event.data.delta, end="", flush=True)
            yield event.data.delta
        else: 
            pass
        