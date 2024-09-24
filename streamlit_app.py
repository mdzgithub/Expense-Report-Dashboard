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

# Calculate KPIs
total_expenses = df['Amount'].sum()
avg_expenses_per_employee = df.groupby('Name')['Amount'].sum().mean()
highest_spender = df.groupby('Name')['Amount'].sum().idxmax()
highest_spender_amount = df.groupby('Name')['Amount'].sum().max()

# Display KPIs
st.header('Expense Report Dashboard')
col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"${total_expenses:.2f}")
col2.metric("Avg Expenses by Employee", f"${avg_expenses_per_employee:.2f}")
col3.metric(f"Highest Spender: {highest_spender}", f"${highest_spender_amount:.2f}")

# Employee filter
employees = ['All'] + list(df['Name'].unique())
selected_employee = st.selectbox('Select Employee', employees)

# Filter data based on selected employee
if selected_employee != 'All':
    filtered_df = df[df['Name'] == selected_employee]
else:
    filtered_df = df

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
st.dataframe(filtered_df, use_container_width=True)