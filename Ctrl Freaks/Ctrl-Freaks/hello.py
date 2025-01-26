import streamlit as st
import streamlit as st
import pandas as pd
import datetime

# Title of the app
st.title("Expense Tracker")

# Sidebar for user input
st.sidebar.header("Add Your Expense")

# Expense category selection
categories = ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Others"]
category = st.sidebar.selectbox("Select Category", categories)

# Amount input
amount = st.sidebar.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")

# Date input
expense_date = st.sidebar.date_input("Expense Date", value=datetime.date.today(), 
                                     min_value=datetime.date(2020, 1, 1), max_value=datetime.date.today())

# Notes (optional)
notes = st.sidebar.text_area("Notes (Optional)")

# Initialize or load expense data
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date", "Notes"])

# Button to submit the expense
if st.sidebar.button("Add Expense"):
    # Validate inputs
    if amount <= 0:
        st.sidebar.error("Amount should be greater than 0.")
    else:
        # Add the expense to the DataFrame
        new_expense = {
            "Category": category,
            "Amount": amount,
            "Date": expense_date,
            "Notes": notes
        }
        st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_expense])], ignore_index=True)
        st.sidebar.success("Expense added successfully!")

# Display current expenses
if st.button("Show Expenses"):
    if st.session_state.expenses.empty:
        st.warning("No expenses recorded yet.")
    else:
        st.subheader("Your Expenses:")
        st.dataframe(st.session_state.expenses)

# Add charts or data visualization (if expenses exist)
if not st.session_state.expenses.empty:
    st.subheader("Expense Breakdown")
    # Group data by category and sum the amounts
    breakdown = st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index()
    st.bar_chart(breakdown.set_index("Category"))
