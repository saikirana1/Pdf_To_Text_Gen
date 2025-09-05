import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio

load_dotenv()


async def multi_agents_manager():
    spanish_agent = Agent(
        name="Spanish Agent", instructions="You translate text to Spanish."
    )
    telugu_agent = Agent(
        name="Telugu Agent", instructions="You translate text to Telugu."
    )

    french_agent = Agent(
        name="French Agent", instructions="You translate text to French."
    )

    italian_agent = Agent(
        name="Italian Agent", instructions="You translate text to Italian."
    )

    manager_agent = Agent(
        name="Manager Agent",
        instructions=(
            "You are a translation manager. "
            "If the user asks for translations, you call the right tools. "
            "Always return the translations clearly."
        ),
        tools=[
            spanish_agent.as_tool(
                tool_name="translate_to_spanish",
                tool_description="Translate the user's message to Spanish",
            ),
            french_agent.as_tool(
                tool_name="translate_to_french",
                tool_description="Translate the user's message to French",
            ),
            italian_agent.as_tool(
                tool_name="translate_to_italian",
                tool_description="Translate the user's message to Italian",
            ),
            telugu_agent.as_tool(
                tool_name="translate_to_telugu",
                tool_description="Translate the user's message to Telugu",
            ),
        ],
    )

    msg = "Translate 'food' into Spanish, French, and Italian and Telugu"

    orchestrator_output = await Runner.run(manager_agent, msg)

    return orchestrator_output.final_output
