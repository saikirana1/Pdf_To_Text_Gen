import streamlit as st
import matplotlib.pyplot as plt


def py_chart(pie_data):
    if pie_data:
        labels = [item["label"] for item in pie_data]
        sizes = [item["value"] for item in pie_data]
    if labels and sizes:
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.subheader("Quantity Distribution (Pie Chart)")
        return st.pyplot(fig)
