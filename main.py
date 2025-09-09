import streamlit as st
from open_ai.synthesizing_data import synthesizing_data
from ai_agents.multi_agent_handoff import multi_agent_handoff

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask Your Query:")

if query:
    st.session_state.messages.append({"query": query})

    result = multi_agent_handoff(query)
    if isinstance(result, tuple):
        final_result = synthesizing_data(query, result[0], result[1])
        st.session_state.messages.append({"final_result": final_result})
    else:
        st.session_state.messages.append({"final_result": result})


for msg in st.session_state.messages:
    if msg.get("query"):
        with st.chat_message("user"):
            st.write(msg["query"])
    if msg.get("final_result"):
        with st.chat_message("ai"):
            st.write(msg["final_result"])
