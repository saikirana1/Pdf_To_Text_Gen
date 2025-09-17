import streamlit as st
from open_ai.synthesizing_data import synthesizing_data
from ai_agents.multi_agent_handoff import multi_agent_handoff
from ai_agents.pdf_agent import pdf_agent
from open_ai.client import openai_client
import json
from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract
from open_ai.pdf_to_text_extract import pdf_to_text_extract
from clean_pdf_data.pdf_json_data import pdf_to_json
from clean_pdf_data.pdf_to_json_data import pdf_to_combined_json
from clean_pdf_data.pdf_plain_text import extract_plain_text_outside_tables
client=openai_client()
if "messages" not in st.session_state:
    st.session_state.messages = []

user_query = st.chat_input("Ask Your Query:")

file_type = st.selectbox(
    "Select the type of file you want to upload:",
    ["Pdf_Text_Document", "Invoice_Pdf", "Bank_Statement_Pdf"],
)


with st.sidebar:
    side_bard = st.selectbox(
        "Select file type:",
        ["Pdf_Text_Document", "Invoice_Pdf", "Bank_Statement_Pdf"],
        key="file_typeggfdg"
    )

uploaded_file = st.file_uploader(
    f"Upload your {file_type}",
    type=["pdf", "jpg", "png", "jpeg", "csv", "xlsx"],  
    key="file_uploader"
)
if side_bard=="PDF_text_document":
   
    if user_query:
        print("i am input prompt",user_query)
        st.session_state.messages.append({"query": user_query})

        query_result = pdf_agent(user_query)
        if isinstance(query_result, tuple):
            final_result = synthesizing_data(user_query, query_result[0], query_result[1])
            st.session_state.messages.append({"final_result": final_result})
        else:
            st.session_state.messages.append({"final_result": query_result})
if side_bard=="Invoice_pdf":
    print("i am invoice")
if side_bard=="Bank_Statement_Pdf":
    if user_query:
        st.session_state.messages.append({"query": user_query})

        query_result = multi_agent_handoff(user_query)
        if isinstance(query_result, tuple):
            final_result = synthesizing_data(user_query, query_result[0], query_result[1])
            st.session_state.messages.append({"final_result": final_result})
        else:
            st.session_state.messages.append({"final_result": query_result})
    print("i am side_bar")
    print("i am bank")
if uploaded_file:
    print("i am uploaded pdf")
    if file_type == "Pdf_Text_Document":
      st.write("Processing Invoice...")
    elif file_type == "Invoice_Pdf":
      file = client.files.create(file=uploaded_file, purpose="user_data")
      data = pdf_to_json_data_extract(file)
      print(data)
    #   print(type(data))
    #   data=pdf_to_json_data_extract(json_data,plain_data)
    elif file_type == "Bank_Statement_Pdf":
      json_data=pdf_to_json(uploaded_file)
      plain_data= extract_plain_text_outside_tables(uploaded_file)
      data=pdf_to_json_data_extract(json_data,plain_data)
      



for msg in st.session_state.messages:
    if msg.get("query"):
        with st.chat_message("user"):
            st.write(msg["query"])
    if msg.get("final_result"):
        with st.chat_message("ai"):
            st.write(msg["final_result"])
