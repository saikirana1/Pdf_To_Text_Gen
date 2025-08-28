import streamlit as st


def key_performance_indicator(data):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Subtotal", f"₹{data.get('subtotal', 0)}")
    col2.metric("SGST", f"₹{data.get('sgst', 0)}")
    col3.metric("CGST", f"₹{data.get('cgst', 0)}")
    col4.metric("Grand Total", f"₹{data.get('total', 0)}")
