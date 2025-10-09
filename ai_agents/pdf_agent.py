from pydantic import BaseModel
from agents import Runner, Agent, function_tool, ModelSettings
from pinecone_v_db.get_db_table import get_db_table
from pinecone_v_db.pinecone_api_client import pinecone_cli

import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, SQLiteSession
load_dotenv()

session = SQLiteSession("simple@gmail.com", "conversation_history.db")
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
        print("i am pdf rag content===========>")
        print(pdf_content)
        # print(results)
       
    except Exception as e:
        return "no result found from rag or technical issue"
    return pdf_content



async def pdf_agent(input_prompt):
    

    rag_agent = Agent(
        name="RAG_AGENT",
        instructions=(
            """You are a retrieval agent. 
        If the user asks any question about uploaded pdf so for this answer go to tool call and 
        get data from their"""
        ),
        tools=[query_chunk],
        handoff_description="""You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer
the question. If you don't know the answer, say that you
don't know. DON'T MAKE UP ANYTHING.
for the context use from tools data

---

Answer the question based on the above context: """,
        model_settings=ModelSettings(tool_choice="query_chunk"),
        tool_use_behavior="run_llm_again",
         model='gpt-4o-mini'
    )
    allocator_agent = Agent(
        name="Allocator",
        instructions="Forward queries to the appropriate agent based on topic.",
        handoffs=[rag_agent],
        model='gpt-4o-mini',
        tool_use_behavior="stop_on_first_tool"

    )

    result = Runner.run_streamed(allocator_agent, input_prompt, session=session)

    print("Active Agent:", result.last_agent.name)
   
    async for event in result.stream_events():
         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            yield event.data.delta
         else:
             pass


