import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Type'])

# Set page config
st.set_page_config(page_title="Books of Accounts", page_icon=":notebook:", layout="wide", initial_sidebar_state="expanded", theme="dark")

# Add header and description
st.title("Books of Accounts / Expense Tracker")
st.markdown("""
    This app is designed to help you maintain your Books of Accounts or track your expenses. You can add new entries using the sidebar, and the app will automatically update the data and insights.
    """)

# Improve data input form
def add_entry(date, description, amount, type):
    new_entry = pd.DataFrame([[date, description, amount, type]], columns=['Date', 'Description', 'Amount', 'Type'])
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)

with st.sidebar.form("Add New Entry"):
    date = st.date_input('Date')
    description = st.text_input('Description')
    amount = st.number_input('Amount', min_value=0.0)
    type = st.selectbox('Type', ['Income', 'Expense'])
    submitted = st.form_submit_button('Add Entry')
    if submitted:
        add_entry(date, description, amount, type)

# Handle missing data
st.session_state.data = st.session_state.data.fillna(value={
    'Date': pd.to_datetime('1900-01-01'),
    'Description': '',
    'Amount': 0.0,
    'Type': ''
})

# Display data
st.subheader("Data")
st.dataframe(st.session_state.data)

# Add more insights
st.subheader("Insights")

# Total balance
total_income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].sum()
total_expenses = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].sum()
total_balance = total_income - total_expenses
st.metric("Total Balance", f"{total_balance:.2f}")

# Average income and expenses
average_income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].mean()
average_expenses = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].mean()
st.metric("Average Income", f"{average_income:.2f}")
st.metric("Average Expenses", f"{average_expenses:.2f}")

# Create a bar plot
fig, ax = plt.subplots()
st.session_state.data.groupby('Type')['Amount'].sum().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Create a heatmap
fig, ax = plt.subplots()
sns.heatmap(st.session_state.data.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Create an interactive line chart
fig = px.line(st.session_state.data, x='Date', y='Amount', color='Type')
st.plotly_chart(fig)

# Cluster income and expenses by amount
kmeans = KMeans(n_clusters=2)
kmeans.fit(st.session_state.data[['Amount'])
st.session_state.data['Cluster'] = kmeans.labels_
st.dataframe(st.session_state.data)
