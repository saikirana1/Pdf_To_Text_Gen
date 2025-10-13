import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import json
from openai import OpenAI


# Initialize OpenAI client
client = OpenAI(
    api_key="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"
)
st.title("📊 PDF Data Analysis with Charts (OpenAI + Streamlit)")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Extract text from PDF
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    st.write("### Extracted Text Preview")
    st.text_area("PDF Content", text[:1000], height=200)

    # Ask OpenAI to convert into structured JSON
    st.write("### Processing with OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analyzer."},
            {
                "role": "user",
                "content": f"""
                Extract only the line items from this text as JSON.
                Format strictly like this:
                [
                  {{"Category": "item description", "Amount": number}},
                  ...
                ]

                Text:
                {text}
                """,
            },
        ],
    )

    # structured_data = response.choices[0].message.content.strip()

    # # Try parsing JSON
    # try:
    #     structured_data = json.loads(structured_data)
    #     df = pd.DataFrame(structured_data)

    #     st.write("### Structured Data from PDF")
    #     st.dataframe(df)

    #     # Pie Chart
    #     st.write("### Pie Chart of Data")
    #     fig, ax = plt.subplots()
    #     ax.pie(df["Amount"], labels=df["Category"], autopct="%1.1f%%", startangle=90)
    #     ax.set_title("PDF Data Distribution")
    #     st.pyplot(fig)

    #     # Bar Chart
    #     st.write("### Bar Chart of Data")
    #     st.bar_chart(df.set_index("Category"))

    # except json.JSONDecodeError as e:
    #     st.error(f"❌ Error parsing JSON from OpenAI: {e}")
    #     st.text(structured_data)  # show raw response for debugging
