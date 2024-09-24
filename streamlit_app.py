import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="Expense Dashboard",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("🎈 Expense Dashboard")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

df = pd.read_csv('/workspaces/Expense-Report-Dashboard/expense-report-2024-09-23T20-59-19Z.csv')

st.dataframe(df)


st.bar_chart(df[['Date', 'Category', 'Amount']],
             x='Category',
             y='Amount')

st.bar_chart(df[['Date', 'Name', 'Amount']],
             x='Name',
             y='Amount')