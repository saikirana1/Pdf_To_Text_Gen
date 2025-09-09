from agents import Runner
import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent
import asyncio

load_dotenv()


def synthesizing_data(question, sql_command, final_result):
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

    result = asyncio.run(
        Runner.run(
            allocator_agent, "Generate the best sentence that the user will understand."
        )
    )
    print(result.final_output)
    return result.final_output
