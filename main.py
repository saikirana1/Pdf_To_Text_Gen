import streamlit as st
from ai_agents.multi_agent_handoff import multi_agent_handoff


def append(msg):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


if "messages" not in st.session_state:
    st.session_state.messages = []


query = st.chat_input("Ask Your Query:")


if query:
    user_msg = {"role": "user", "content": query}
    st.session_state.messages.append(user_msg)
    append(user_msg)

    result = multi_agent_handoff(query)
    ai_msg = {"role": "ai", "content": result}
    st.session_state.messages.append(ai_msg)
    append(ai_msg)
