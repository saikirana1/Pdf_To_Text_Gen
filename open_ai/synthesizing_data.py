from .client import openai_client
from pydantic import BaseModel

client = openai_client()


def synthesizing_data(user_prompt: str, sql_query: str, db_result: str):
    class Chat(BaseModel):
        answer: str

    print("Process started...")

    completion = client.chat.completions.parse(
        model="gpt-5-nano",
        # gpt-5-mini
        messages=[
            {
                "role": "user",
                "content": f"""
You are a data assistant. 
I will give you three things:
1. A user prompt: "{user_prompt}"
2. The SQL query generated: "{sql_query}"
3. The database result: "{db_result}"

Your task:
- Combine these pieces of information don't use any symbol doller , rupee anything else give just number.
don't write in words 
don't confuise with the id and transaction_id
here simple context and use the data
- Provide a clear, human-understandable answer to the user based on the database result.
- Do not invent information that is not present.
                """,
            }
        ],
        response_format=Chat,
    )

    result: Chat = completion.choices[0].message.parsed
    data = result.answer
    return data
