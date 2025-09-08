from .client import openai_client
from pydantic import BaseModel

client = openai_client()


def synthesizing_data(user_prompt: str, sql_query: str, db_result: str):
    class Chat(BaseModel):
        answer: str

    print("Process started...")

    completion = client.chat.completions.parse(
        model="gpt-5-nano",
        # gpt-5-mini
        messages=[
            {
                "role": "user",
                "content": f"""
You are a data assistant. 
I will give you three things:
1. A user prompt: "{user_prompt}"
2. The SQL query generated: "{sql_query}"
3. The database result: "{db_result}"

Your task:
- Combine these pieces of information don't use any symbol doller , rupee anything else give just number.
don't write in words 
don't confuise with the id and transaction_id
here simple context and use the data
- Provide a clear, human-understandable answer to the user based on the database result.
- Do not invent information that is not present.
                """,
            }
        ],
        response_format=Chat,
    )

    result: Chat = completion.choices[0].message.parsed
    data = result.answer
    return data


from open_ai.llm_sql_query import llm_sql_query
from database_sql.query_data import query_data
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
        sql_query = result[1]
        db_result = result[0]
        final_result = synthesizing_data(query, sql_query, db_result)
    # print("sql_query", sql_query)
    # sql_text = f"Generated SQL:\n```sql\n{sql_query}\n```"
    # st.session_state.messages.append({"sql_text": sql_text})

    # query_result = query_data(sql_query)
    # print("query_result", query_result)

    st.session_state.messages.append({"final_result": result})

    if isinstance(result, tuple):
        print(final_result, "iugi")
        st.session_state.messages.append({"final_result": final_result})


for msg in st.session_state.messages:
    if msg.get("query"):
        with st.chat_message("user"):
            st.write(msg["query"])
    # if msg.get("sql_text"):
    #     with st.chat_message("ai"):
    #         st.write(msg["sql_text"])
    if msg.get("final_result"):
        with st.chat_message("ai"):
            st.write(msg["final_result"])
