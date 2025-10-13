# from openai import OpenAI
# import math


# # client = OpenAI()
# from open_ai.client import openai_client

# client = openai_client()


# def calculator(expression: str):
#     try:
#         return str(eval(expression))
#     except Exception as e:
#         return f"Error: {e}"


# # Agent function
# def simple_agent(user_input: str):
#     # Step 1: Ask GPT what to do
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful agent that can use a calculator tool.",
#             },
#             {"role": "user", "content": user_input},
#         ],
#         tools=[
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "calculator",
#                     "description": "Evaluate a math expression",
#                     "parameters": {
#                         "type": "object",  # 👈 must always be "object"
#                         "properties": {
#                             "expression": {
#                                 "type": "string",
#                                 "description": "A math expression like '25*25' or 'sqrt(144)'",
#                             }
#                         },
#                         "required": ["expression"],
#                     },
#                 },
#             }
#         ],
#     )

#     # Step 2: Check if GPT called the tool
#     message = response.choices[0].message
#     if message.tool_calls:
#         for tool_call in message.tool_calls:
#             if tool_call.function.name == "calculator":
#                 # tool_call.function.arguments is a JSON string → parse it
#                 import json

#                 args = json.loads(tool_call.function.arguments)
#                 expr = args["expression"]

#                 result = calculator(expr)

#                 # Step 3: Return result
#                 return f"Answer: {result}"

#     # If GPT didn’t call the tool, just return text
#     return message.content

from agents import Agent, Runner, function_tool
from pydantic import BaseModel


class Query(BaseModel):
    query: str


# @function_tool
# def solve_addition(a: int, b: int) -> int:
#     return a + b


def demo():
    agent = Agent(
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

            For a given input, write an simple and accurate PostgreSQL query to run against the database.""",
        output_type=Query,
    )

    query = "what is the my  total  withdrawal amount "

    result = Runner.run_sync(agent, query)

    print(result.final_output.query)

    return


from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)


async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
