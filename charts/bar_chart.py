import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def bar_chart_revenue_per_product(bar_data: list):
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


def bar_chart_quantity_per_category(cat_summary):
    fig, ax = plt.subplots()
    ax.bar(cat_summary["Category"], cat_summary["Qty"])
    ax.set_ylabel("Quantity")
    ax.set_title("Quantity per Category")
    st.subheader("Category-Level Quantity Distribution")
    return st.pyplot(fig)


def bar_chart_revenue_per_category(cat_summary):
    fig, ax = plt.subplots()
    ax.bar(cat_summary["Category"], cat_summary["Amount"])
    ax.set_ylabel("Revenue (₹)")
    ax.set_title("Revenue per Category")
    st.subheader("Category-Level Revenue Distribution")
    st.pyplot(fig)
