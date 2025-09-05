from open_ai.llm_sql_query import llm_sql_query
from database_sql.query_data import query_data
import streamlit as st
from open_ai.synthesizing_data import synthesizing_data

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask Your Query:")

if query:
    st.session_state.messages.append({"query": query})

    sql_query = llm_sql_query(query)
    print("sql_query", sql_query)
    sql_text = f"Generated SQL:\n```sql\n{sql_query}\n```"
    st.session_state.messages.append({"sql_text": sql_text})

    query_result = query_data(sql_query)
    print("query_result", query_result)
    final_result = synthesizing_data(query, sql_query, query_result)
    st.session_state.messages.append({"final_result": final_result})


for msg in st.session_state.messages:
    if msg.get("query"):
        with st.chat_message("user"):
            st.write(msg["query"])
    if msg.get("sql_text"):
        with st.chat_message("ai"):
            st.write(msg["sql_text"])
    if msg.get("final_result"):
        with st.chat_message("ai"):
            st.write(msg["final_result"])
