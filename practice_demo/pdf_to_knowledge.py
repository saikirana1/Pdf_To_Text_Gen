from openai import OpenAI
import streamlit as st
import matplotlib.pyplot as plt
import json
import pandas as pd

client = OpenAI(
    api_key="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"
)


st.title("📑 Invoice Dashboard")

# Upload PDF
uploaded_file = st.file_uploader("Upload an Invoice PDF", type=["pdf"])

if uploaded_file:
    # Send file to OpenAI
    file = client.files.create(file=uploaded_file, purpose="user_data")

    # Ask model to extract JSON
    completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": file.id}},
                    {
                        "type": "text",
                        "text": """Extract invoice details as JSON dictionary with fields:
                        - items: list of dicts { "Description", "Qty", "UnitPrice", "Amount" }
                        - subtotal
                        - sgst
                        - cgst
                        - total
                        - piechartdata: list of dicts { "label": Description, "value": Qty }
                        - barchartdata: list of dicts { "label": Description, "value": Amount }
                        """,
                    },
                ],
            }
        ],
    )

    response_text = completion.choices[0].message.content

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        data = json.loads(response_text[start:end])

    # -------------------
    # 📌 Show Invoice KPIs
    # -------------------
    print(data)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Subtotal", f"₹{data.get('subtotal', 0)}")
    col2.metric("SGST", f"₹{data.get('sgst', 0)}")
    col3.metric("CGST", f"₹{data.get('cgst', 0)}")
    col4.metric("Grand Total", f"₹{data.get('total', 0)}")

    # -------------------
    # 📊 Pie Chart (Quantities per Product)
    # -------------------
    pie_data = data.get("piechartdata", [])
    if pie_data:
        labels = [item["label"] for item in pie_data]
        sizes = [item["value"] for item in pie_data]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.subheader("Quantity Distribution (Pie Chart)")
        st.pyplot(fig)

    # -------------------
    # 📊 Bar Chart (Revenue per Product swdkljf)
    # -------------------
    bar_data = data.get("barchartdata", [])
    if bar_data:
        df = pd.DataFrame(bar_data)
        fig, ax = plt.subplots()
        ax.bar(df["label"], df["value"])
        ax.set_ylabel("Amount (₹)")
        ax.set_xlabel("Products")
        ax.set_title("Revenue by Product")
        plt.xticks(rotation=45, ha="right")
        st.subheader("Revenue Distribution (Bar Chart)")
        st.pyplot(fig)

    # -------------------
    # 📊 Category-Level Analysis
    # -------------------
    items = data.get("items", [])
    if items:
        df_items = pd.DataFrame(items)

        # Define categories by description keywords
        def categorize(desc):
            desc = desc.lower()
            if "mini tub" in desc:
                return "Mini Tub"
            elif "big lolly" in desc:
                return "Big Lolly"
            elif "4 ltr" in desc:
                return "4 LTR"
            elif "fp premium" in desc:
                return "FP Premium"
            else:
                return "Others"

        df_items["Category"] = df_items["Description"].apply(categorize)

        # Group by category
        cat_summary = (
            df_items.groupby("Category")
            .agg({"Qty": "sum", "Amount": "sum"})
            .reset_index()
        )

        # Bar Chart - Quantity per Category
        fig, ax = plt.subplots()
        ax.bar(cat_summary["Category"], cat_summary["Qty"])
        ax.set_ylabel("Quantity")
        ax.set_title("Quantity per Category")
        st.subheader("Category-Level Quantity Distribution")
        st.pyplot(fig)

        # Bar Chart - Revenue per Category
        fig, ax = plt.subplots()
        ax.bar(cat_summary["Category"], cat_summary["Amount"])
        ax.set_ylabel("Revenue (₹)")
        ax.set_title("Revenue per Category")
        st.subheader("Category-Level Revenue Distribution")
        st.pyplot(fig)

    # -------------------
    # 📑 Raw JSON Data
    # -------------------
    with st.expander("Extracted Invoice Data (Raw JSON)"):
        st.json(data)
