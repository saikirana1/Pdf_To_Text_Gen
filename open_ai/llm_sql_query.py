from .client import openai_client
from pydantic import BaseModel
from enum import Enum

client = openai_client()


class Presentation(Enum):
    table = "table"
    text = "text"


class SqlQuery(BaseModel):
    query: str

    """How to present the response from the SQL query"""
    output_presentation: Presentation


def llm_sql_query(prompt: str):
    print("Process started...")

    completion = client.responses.parse(
        model="gpt-5-mini",
        instructions="""
You are an expert at writing SQL queries for PostgreSQL database with the following schema:

CREATE TABLE transaction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id VARCHAR(255),
    transaction_date DATE,
    withdrawal NUMERIC,
    deposit NUMERIC,
    balance NUMERIC,
    description TEXT
);

For a given input, write an simple and accurate PostgreSQL query to run against the database.
""",
        input=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        text_format=SqlQuery,
    )

    result: SqlQuery = completion.output_parsed
    data = result.query
    print(result)
    return data
