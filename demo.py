import streamlit as st

# st.title("Hello, Streamlit!")
# st.write("This is my first Streamlit app.")
# st.write("This is sai kiran")
# st.write("Hi Nellore")


st.header("i am header")
st.subheader("This is sub Header")
st.text("This is the")
st.markdown("This is **bold**, *italic*, and [a link](https://streamlit.io)")
st.caption("This is a **small**, *caption* text.")
st.code("print('Hello World')", language="python")
st.latex(r"E = mc^2")


import streamlit as st
import pandas as pd

st.title("Text Formatting with Lists & Tables")

st.header("📋 Example List")
st.markdown("""
- Item 1
- Item 2
- Item 3
""")

st.header("🔢 Numbered List")
st.markdown("""
1. Step One
2. Step Two
3. Step Three
""")

st.header("📊 Example Table (Markdown)")
st.markdown("""
| Name   | Age | City     |
|--------|-----|----------|
| Alice  | 24  | London   |
| Bob    | 30  | New York |
| Carol  | 27  | Paris    |
""")

st.header("📊 Example Table (Pandas)")
df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Carol"],
        "Age": [24, 30, 27],
        "City": ["London", "New York", "Paris"],
    }
)
st.write(df)
