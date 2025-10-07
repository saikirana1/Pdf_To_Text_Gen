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
    print(question)
    print(sql_command)
    print(final_result, "--------------->")
    synthesize_data = Agent(
        name="Synthesize Data",
        handoff_description=(
            "You are a specialist agent responsible for converting raw SQL query results "
            "into clear, human-understandable sentences."
        ),
        instructions=f"""
            The user asked: "{question}"
            The executed SQL query is: {sql_command}
            The SQL result is: {final_result}

            Your task:
            - Understand the question, SQL query, and its result.
            - Interpret the data and respond in plain, easy-to-understand English.
            - Avoid technical terms, database jargon, or raw values unless necessary.
            - Do NOT use any currency symbols or unnecessary formatting.
            - If the result is a list or dictionary, summarize it meaningfully.

            Example:
            Q: "How many invoices do I have?"
            SQL Result: 5
            Response: "You have 5 invoices in total."
            """,
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
            print(event.data.delta, end="", flush=True)
            # print(event.data)
            yield event.data.delta
        else: 
            pass
        