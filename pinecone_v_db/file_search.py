from agents import Agent, Runner, FileSearchTool
from openai import OpenAI
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# Point FileSearchTool to your Pinecone index
file_search = FileSearchTool(
    max_num_results=3,
    vector_store_ids=["knowledge"],  # same as your Pinecone index name
)

agent = Agent(
    name="File Assistant",
    tools=[file_search],
)


async def main():
    result = await Runner.run(agent, "Tell me something about machine learning")
    return result
