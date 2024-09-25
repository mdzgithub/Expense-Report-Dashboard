import streamlit as st
import pandas as pd
import altair as alt
import config
from databricks import sql

# Load the data
@st.cache_data
def load_data():
    try:
        connection = sql.connect(
            server_hostname=config.server_hostname,
            http_path=config.http_path,
            access_token=config.access_token
        )

        # Use pandas to read SQL query directly into a DataFrame
        df = pd.read_sql("SELECT * FROM hive_metastore.default.expense_gold", connection)
        
        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df

    except Exception as e:
        st.error(f"An error occurred while loading data: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
    finally:
        if 'connection' in locals():
            connection.close()

# Load data
df = load_data()

# Check if the DataFrame is empty
if df.empty:
    st.warning("No data available. Please check your database connection and query.")
    st.stop()  # Stop the app here if there's no data

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