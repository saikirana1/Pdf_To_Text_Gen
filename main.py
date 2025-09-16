import streamlit as st
from open_ai.synthesizing_data import synthesizing_data
from ai_agents.multi_agent_handoff import multi_agent_handoff
from open_ai.client import openai_client
import json
from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract


client=openai_client()
if "messages" not in st.session_state:
    st.session_state.messages = []

user_query = st.chat_input("Ask Your Query:")
file_type = st.selectbox(
    "Select the type of file you want to upload:",
    ["PDF", "Invoice", "Bank Statement"]
)
uploaded_file = st.file_uploader(
    f"Upload your {file_type}",
    type=["pdf", "jpg", "png", "jpeg", "csv", "xlsx"],  
    key="file_uploader"
)
if uploaded_file:
    if file_type == "PDF":
      file = client.files.create(file=uploaded_file, purpose="user_data")
      data = pdf_to_json_data_extract(file)
      print(data)
      print(type(data))
    elif file_type == "Invoice":
        st.write("Processing Invoice...")
    elif file_type == "Bank Statement":
        st.write(" Processing Bank Statement...")

if user_query:
    st.session_state.messages.append({"query": user_query})

    query_result = multi_agent_handoff(user_query)
    if isinstance(query_result, tuple):
        final_result = synthesizing_data(user_query, query_result[0], query_result[1])
        st.session_state.messages.append({"final_result": final_result})
    else:
        st.session_state.messages.append({"final_result": query_result})


for msg in st.session_state.messages:
    if msg.get("query"):
        with st.chat_message("user"):
            st.write(msg["query"])
    if msg.get("final_result"):
        with st.chat_message("ai"):
            st.write(msg["final_result"])
