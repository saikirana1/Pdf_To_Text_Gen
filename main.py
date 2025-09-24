# import streamlit as st
# from open_ai.synthesizing_data import synthesizing_data
# from ai_agents.multi_agent_handoff import multi_agent_handoff
from open_ai.client import openai_client
# import json
# from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract
# from practice_demo.pdf_to_text_extract import pdf_to_text_extract
# from clean_pdf_data.pdf_json_data import pdf_to_json
# from clean_pdf_data.pdf_to_json_data import pdf_to_combined_json
# from clean_pdf_data.pdf_plain_text import extract_plain_text_outside_tables
# from ai_agents.invoice_data_agent import invoice_data_agent
# from pinecone_v_db.insert_chunks import insert_chunks
# from open_ai.create_pdf_embedings import create_pdf_embedings
# from pinecone_v_db.query_chunk import  query_check
# from open_ai.invoice_pdf_to_json import invoice_pdf_json
# import asyncio
# from openai.types.responses import ResponseTextDeltaEvent
# from agents import Agent, Runner
client=openai_client()
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# user_query = st.chat_input("Ask Your Query:")

# file_type = st.selectbox(
#     "Select the type of file you want to upload:",
#     ["Pdf_Text_Document", "Invoice_Pdf", "Bank_Statement_Pdf"],
# )


# with st.sidebar:
#     side_bard = st.selectbox(
#         "Select file type:",
#         ["Pdf_Text_Document", "Invoice_Pdf", "Bank_Statement_Pdf"],
#         key="file_typeggfdg"
#     )

# uploaded_file = st.file_uploader(
#     f"Upload your {file_type}",
#     type=["pdf", "jpg", "png", "jpeg", "csv", "xlsx"],  
#     key="file_uploader"
# )
# if side_bard=="Pdf_Text_Document":
   
#     if user_query:
#         print("i am input prompt",user_query)
#         st.session_state.messages.append({"query": user_query})

#         query_result = pdf_agent(user_query)
#         if isinstance(query_result, tuple):
#             final_result = synthesizing_data(user_query, query_result[0], query_result[1])
#             st.session_state.messages.append({"final_result": final_result})
#         else:
#             st.session_state.messages.append({"final_result": query_result})
# if side_bard=="Invoice_Pdf":
#      print("i am invoice")
#      if user_query:
#         print("i am input prompt",user_query)
#         st.session_state.messages.append({"query": user_query})

#         query_result = invoice_data_agent(user_query)
#         print(query_result)
#         if isinstance(query_result, tuple):
#             final_result = synthesizing_data(user_query, query_result[0], query_result[1])
#             st.session_state.messages.append({"final_result": final_result})
#         else:
#             st.session_state.messages.append({"final_result": query_result})
    
# if side_bard=="Bank_Statement_Pdf":
#     if user_query:
#         st.session_state.messages.append({"query": user_query})

#         query_result = multi_agent_handoff(user_query)
#         if isinstance(query_result, tuple):
#             final_result = synthesizing_data(user_query, query_result[0], query_result[1])
#             st.session_state.messages.append({"final_result": final_result})
#         else:
#             st.session_state.messages.append({"final_result": query_result})
#     print("i am side_bar")
#     print("i am bank")
# if uploaded_file:
#     print("i am uploaded pdf")
#     if file_type == "Pdf_Text_Document":
#     #   st.session_state["uploaded_pdf"] = None
#       pdf_chunks=create_pdf_embedings(uploaded_file)
#       insert_chunks(pdf_chunks)
#     elif file_type == "Invoice_Pdf":
#       file = client.files.create(file=uploaded_file, purpose="user_data")
#       data = invoice_pdf_json(file)
#       print(data)
#     #   print(type(data))
#     #   data=pdf_to_json_data_extract(json_data,plain_data)
#     elif file_type == "Bank_Statement_Pdf":
#       json_data=pdf_to_json(uploaded_file)
#       plain_data= extract_plain_text_outside_tables(uploaded_file)
#       data=pdf_to_json_data_extract(json_data,plain_data)

# for msg in st.session_state.messages:
#     if msg.get("query"):
#         with st.chat_message("user"):
#             st.write(msg["query"])
#     if msg.get("final_result"):
#         with st.chat_message("ai"):
#             st.write(msg["final_result"])







# async def main():
#     agent = Agent(
#         name="FunnyBot",
#         instructions="You are a helpful assistant who tells jokes."
#     )

#     result = Runner.run_streamed(agent, input="what is java")

#     # Stream token by token
#     async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#             # Print tokens as they arrive (like typing effect)
#             print(event.data.delta, end="", flush=True)

# if __name__ == "__main__":
#     asyncio.run(main())


# from services import get_data

# if __name__ == "__main__":
#     result = get_data()
#     print(result)
#     data=result.model_dump_json()
#     print(result.model_dump)   # Convert to dictionary
#     print(result.model_dump_json())
#     print(data.get("position"))   # Convert to JSON string

from ai_agents.pdf_agent import pdf_agent  # noqa: E402

t=pdf_agent("what is python")
print(t)