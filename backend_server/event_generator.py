from ..open_ai.synthesizing_data import synthesizing_data
from ..ai_agents.pdf_agent import pdf_agent
async def event_generator(user_question,sql_query,sql_result):
                    async for chunk in synthesizing_data(user_question, sql_query, sql_result):
               
                     print(chunk, end="", flush=True)
                     yield f"data: {chunk}\n\n"
    
async def event_generator_pdf(user_prompt):
                    print("from event pdf saasdkljdfsdfkj======>")
                    async for chunk in pdf_agent(user_prompt):
               
                     print(chunk, end="", flush=True)
                     yield f"data: {chunk}\n\n"