from agents import Runner
import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent

load_dotenv()

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

allocator_agent = Agent(
    name="Allocator Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
)


result = Runner.run_sync(allocator_agent, "What is the capital of India?")
print(result.final_output)
