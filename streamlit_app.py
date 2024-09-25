import streamlit as st
import pandas as pd
import altair as alt

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('expense-report-2024-09-23T20-59-19Z.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar
st.sidebar.header('Filters')

# Date range filter
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
start_date = st.sidebar.date_input('Start date', min_date)
end_date = st.sidebar.date_input('End date', max_date)

# Employee filter
employees = ['All'] + list(df['Name'].unique())
selected_employee = st.sidebar.selectbox('Select Employee', employees)

# Filter data based on date range and selected employee
filtered_df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
if selected_employee != 'All':
    filtered_df = filtered_df[filtered_df['Name'] == selected_employee]

# Calculate KPIs
total_expenses = filtered_df['Amount'].sum()
avg_expenses_per_employee = filtered_df.groupby('Name')['Amount'].sum().mean()
highest_spender = filtered_df.groupby('Name')['Amount'].sum().idxmax()
highest_spender_amount = filtered_df.groupby('Name')['Amount'].sum().max()

# Display KPIs
st.header('Expense Report Dashboard')
col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"${total_expenses:.2f}")
col2.metric("Avg Expenses by Employee", f"${avg_expenses_per_employee:.2f}")
col3.metric(f"Highest Spender: {highest_spender}", f"${highest_spender_amount:.2f}")

# Create bar chart
chart_data = filtered_df.groupby('Category')['Amount'].sum().reset_index()
chart = alt.Chart(chart_data).mark_bar().encode(
    x='Category',
    y='Amount',
    color='Category'
).properties(
    title='Expenses by Category'
)

st.altair_chart(chart, use_container_width=True)

# Display raw data
st.subheader('Raw data')
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)