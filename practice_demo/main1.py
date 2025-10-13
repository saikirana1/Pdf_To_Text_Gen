import streamlit as st
import pandas as pd
from open_ai.client import openai_client
from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract
from pdf_highlights_data.key_performance_indicator import key_performance_indicator
from charts.pie_chart import py_chart
from charts.bar_chart import (
    bar_chart_revenue_per_product,
    categorize,
    bar_chart_quantity_per_category,
    bar_chart_revenue_per_category,
)

client = openai_client()
st.header("Welcome to Konic")

st.title("📑 Invoice Dashboard")


def pdf_to_knowledge(uploaded_file):
    if uploaded_file:
        file = client.files.create(file=uploaded_file, purpose="user_data")
        data = pdf_to_json_data_extract(file)

        print(data)
        key_performance_indicator(data)

        pie_data = data.get("piechartdata", [])
        print()
        if pie_data:
            py_chart(pie_data)

        bar_data = data.get("barchartdata", [])
        if bar_data:
            bar_chart_revenue_per_product(bar_data)

        items = data.get("items", [])
        if items:
            df_items = pd.DataFrame(items)

            df_items["Category"] = df_items["Description"].apply(categorize)

            cat_summary = (
                df_items.groupby("Category")
                .agg({"Qty": "sum", "Amount": "sum"})
                .reset_index()
            )

            bar_chart_quantity_per_category(cat_summary)

            bar_chart_revenue_per_category(cat_summary)

        with st.expander("Extracted Invoice Data (Raw JSON)"):
            st.json(data)


with st.form(key="chat_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Upload an Invoice PDF", type=["pdf"])
    submit_button = st.form_submit_button("Upload")


if submit_button and uploaded_file:
    with st.spinner("Processing file, please wait..."):
        pdf_to_knowledge(uploaded_file)
    st.success("File uploaded and processed!")

query = st.chat_input("Ask Your Query:")
