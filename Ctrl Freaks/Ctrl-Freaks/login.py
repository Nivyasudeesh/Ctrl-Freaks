import streamlit as st

# Set the title of the web page
st.title("Login Page")

# Add a description
st.write("Please enter your username and password to log in.")

# Create two text input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")  # Type 'password' hides input

# Create a login button
login_button = st.button("Login")

# Set hardcoded login credentials for simplicity
valid_username = "user123"
valid_password = "password123"

# Logic for login validation
if login_button:
    if username == valid_username and password == valid_password:
        st.success("Login successful!")
        # You can add more actions after successful login, e.g., redirect or show another page
        st.write("Welcome to the app!")
    elif username != valid_username:
        st.error("Invalid username. Please try again.")
    elif password != valid_password:
        st.error("Invalid password. Please try again.")
