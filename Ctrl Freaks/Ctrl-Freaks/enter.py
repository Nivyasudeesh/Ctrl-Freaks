import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# SQLite Database connection
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

# Initialize Database
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    conn.commit()

# Initialize database
init_db()

# Streamlit Session state to store user authentication
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Utility function to execute a query and fetch results
def fetch_query(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchall()

# User login functionality
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = fetch_query('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
        if user:
            st.session_state['user_id'] = user[0][0]
            st.success(f"Welcome {username}")
            return True
        else:
            st.error("Invalid credentials")
            return False

# User registration functionality
def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password != confirm_password:
        st.error("Passwords do not match")

    if st.button("Register"):
        existing_user = fetch_query('SELECT * FROM user WHERE username = ?', (username,))
        if existing_user:
            st.error("Username already exists")
        else:
            cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            st.success("User registered successfully! You can now log in.")

# Function to add a new expense
def add_expense():
    st.title("Add New Expense")
    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    category = st.text_input("Category")
    date = st.date_input("Date", min_value=datetime.today())
    
    if st.button("Add Expense"):
        cursor.execute('INSERT INTO expense (name, amount, category, date, user_id) VALUES (?, ?, ?, ?, ?)', 
                       (name, amount, category, date, st.session_state['user_id']))
        conn.commit()
        st.success("Expense added successfully!")

# Function to edit an existing expense
def edit_expense(expense_id):
    st.title("Edit Expense")
    expense = fetch_query('SELECT * FROM expense WHERE id = ?', (expense_id,))[0]
    
    name = st.text_input("Expense Name", expense[1])
    amount = st.number_input("Amount", min_value=0.01, format="%.2f", value=expense[2])
    category = st.text_input("Category", expense[3])
    date = st.date_input("Date", value=datetime.strptime(expense[4], '%Y-%m-%d').date())
    
    if st.button("Update Expense"):
        cursor.execute('UPDATE expense SET name = ?, amount = ?, category = ?, date = ? WHERE id = ?',
                       (name, amount, category, date, expense_id))
        conn.commit()
        st.success("Expense updated successfully!")

# Function to delete an expense
def delete_expense(expense_id):
    cursor.execute('DELETE FROM expense WHERE id = ?', (expense_id,))
    conn.commit()
    st.success("Expense deleted successfully!")

# Function to display all expenses
def display_expenses():
    st.title("Your Expenses")
    expenses = fetch_query('SELECT * FROM expense WHERE user_id = ?', (st.session_state['user_id'],))
    if not expenses:
        st.write("No expenses found.")
    else:
        df = pd.DataFrame(expenses, columns=["ID", "Name", "Amount", "Category", "Date", "User ID"])
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        st.dataframe(df)
        selected_expense_id = st.selectbox("Select an expense to edit or delete", df["ID"])
        
        if selected_expense_id:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit Expense"):
                    edit_expense(selected_expense_id)
            with col2:
                if st.button("Delete Expense"):
                    delete_expense(selected_expense_id)

# Main function to handle the app
def main():
    if st.session_state['user_id'] is None:
        st.sidebar.title("Authentication")
        choice = st.sidebar.radio("Choose an option", ["Login", "Register"])
        
        if choice == "Login":
            if login():
                st.sidebar.success("Logged in successfully!")
                display_expenses()
        elif choice == "Register":
            register()
    else:
        st.sidebar.title("Expense Tracker")
        st.sidebar.write("Welcome back!")
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update(user_id=None))
        
        choice = st.sidebar.radio("Choose an action", ["View Expenses", "Add New Expense"])
        
        if choice == "View Expenses":
            display_expenses()
        elif choice == "Add New Expense":
            add_expense()

if __name__ == "__main__":
    main()
