from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from ..pinecone_v_db.get_db_table import get_db_table
from ..pinecone_v_db.pinecone_api_client import pinecone_cli
from ..database_sql.query_data import query_data
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from .run_rag_sql_agent import run_rag_agent
load_dotenv()


@function_tool
def query_chunk(text: str) -> dict:
    
    try:
        db, table = get_db_table()
        table="pdf_chunks"
        pc = pinecone_cli()
        index = pc.Index(db)
        results = index.search(
            namespace=table, query={"inputs": {"text": text}, "top_k": 1}
        )
       
        pdf_content = results["result"]["hits"][0]["fields"]["page_content"]
        print("i am pdf rag content")
        print(results)
       
    except Exception as e:
        return "no result found from rag or technical issue"
    return pdf_content


class Result(BaseModel):
    answer: str


async def pdf_agent(input_prompt):
    

    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question about uploaded pdf so for this answer go to tool call and 
        get data from their"""
        ),
        tools=[query_chunk],
        output_type=Result,
        handoff_description=f"""You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer
the question. If you don't know the answer, say that you
don't know. DON'T MAKE UP ANYTHING.
for the context use from tools data

---

Answer the question based on the above context: {input_prompt} """,
        model_settings=ModelSettings(tool_choice="query_chunk"),
        tool_use_behavior="run_llm_again",
         model='gpt-4o-mini'
    )

    casual_agent = Agent(
        name="Casual_Agent",
        instructions="You speak with the user in a casual tone and respond with delightful messages",
        handoff_description="When user speaks casually with things like hello, hi etc, you carry a casual conversation with the user",
        model='gpt-4o-mini'
    )

    allocator_agent = Agent(
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[rag_agent, casual_agent],
        model='gpt-4o-mini'
    )

    result = await Runner.run(allocator_agent, input_prompt,max_turns=50)

    print("Active Agent:", result.last_agent.name)
   
    if result.last_agent.name == "RAG_AGENT":
        print(result.final_output)
        return result.last_agent.name,result.final_output.answer
    elif result.last_agent.name == "Casual_Agent":
        return result.last_agent.name,result.final_output
    return "None , your asking quations out of the subject"
