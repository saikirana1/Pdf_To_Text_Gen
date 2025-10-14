from open_ai.synthesizing_data import synthesizing_data
from open_ai.invoice_rag_result import invoice_rag_result
from ai_agents.pdf_agent import pdf_agent
from open_ai.file_data_synthesis import file_data_synthesis
async def event_generator(user_question,sql_query,sql_result):
                    async for chunk in synthesizing_data(user_question, sql_query, sql_result):
               
                     print(chunk, end="", flush=True)
                     yield f"data: {chunk}\n\n"
    
async def event_generator_pdf(user_prompt):
                    print("from event pdf saasdkljdfsdfkj======>")
                    async for chunk in pdf_agent(user_prompt):
               
                     print(chunk, end="", flush=True)
                     yield f"data: {chunk}\n\n"


async def event_generator_rag(user_question):
    print(user_question)
    async for chunk in invoice_rag_result(user_question):
        print(chunk, end="", flush=True)
        yield f"data: {chunk}\n\n"


async def event_generator_file(user_question, urls):
    print(user_question)
    async for chunk in file_data_synthesis(user_question, urls):
        print(chunk, end="", flush=True)
        yield f"data: {chunk}\n\n"
