import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent
from agents import Runner

load_dotenv()


def hi():
    weather_agent = Agent(
        name="Weather Agent", instructions="Answer questions about weather conditions."
    )

    news_agent = Agent(
        name="News Agent", instructions="Answer questions about current news events."
    )

    # Allocator agent decides which agent should answer
    allocator_agent = Agent(
        name="Allocator",
        instructions="Decide which agent to forward the question to based on its topic.",
        handoffs=[weather_agent, news_agent],
    )

    # Example queries
    query1 = "Will it rain tomorrow in mumbai?"
    query2 = "Who won the football match yesterday?"

    # Run the allocator agent
    result1 = Runner.run_sync(allocator_agent, query1)
    result2 = Runner.run_sync(allocator_agent, query2)

    print(result1.final_output)
    print(result2.final_output)
    return
