from agents import Runner
import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()


async def synthesizing_rag_data(question, answer):
    synthesize_data = Agent(
        name="Synthesize Data",
        handoff_description=f"""
        Specialist agent for synthesizing data.
        This is the user question: {question},
     
        and this is the answer for the quation: {answer}.
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
        allocator_agent, "Generate the best sentence that the user will understand."
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            yield event.data.delta
        else:
            pass
