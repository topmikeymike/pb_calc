import os
import json
from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu

# Functions to handle user data
def get_user_data():
    """Load user data from a JSON file."""
    if not os.path.exists("users.json"):
        return {"users": [], "current_users": 0}
    with open("users.json", "r") as file:
        return json.load(file)

def save_user_data(data):
    """Save user data to a JSON file."""
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)

def add_user(username):
    """Add a new user to the database."""
    data = get_user_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["users"].append({"username": username, "timestamp": timestamp})
    data["current_users"] += 1
    save_user_data(data)

def remove_user():
    """Remove a user (decrease real-time user count)."""
    data = get_user_data()
    if data["current_users"] > 0:
        data["current_users"] -= 1
    save_user_data(data)

# Streamlit App Configuration
st.set_page_config(page_title="Pendapatan Bersih Calculator", page_icon="📊", layout="centered")

# Custom CSS for Aesthetic Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stNumberInput > label {
        font-weight: bold;
        color: #333;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
    .highlighted {
        font-size: 24px;
        font-weight: bold;
        color: #FF5733;
        background-color: #FFF3E0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home", "About"],
        icons=["house", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

    # User Login
    username = st.text_input("Enter your username:", value="", placeholder="Type your name here")
    if username:
        add_user(username)
        st.success(f"Welcome, {username}! You are now using the app.")
    else:
        st.warning("Please enter your username to proceed.")

# Load user data
user_data = get_user_data()

if selected == "Home":
    # Title and Description
    st.title("📊 Pendapatan Bersih Calculator")
    st.write("Welcome! Use this tool to calculate your **Pendapatan Bersih (Net Income)** with ease and clarity.")
    st.markdown("---")

    # Input Fields
    st.header("Input Details")
    pendapatan_kasar = st.number_input("Pendapatan Kasar (Gross Income) in RM:", min_value=0, value=0, step=1)
    total_firstaid = st.number_input("Total First Aid Count:", min_value=0, value=0, step=1)
    whitezone = st.number_input("Total Whitezone Count:", min_value=0, value=0, step=1)
    event = st.number_input("Total Event Count:", min_value=0, value=0, step=1)

    # Calculations
    TOTAL_FIRST_AID = total_firstaid * 200
    TOTAL_WHITEZONE = whitezone * 50
    TOTAL_EVENT = event * 50
    PENDAPATAN_BERSIH = pendapatan_kasar - TOTAL_FIRST_AID - TOTAL_WHITEZONE - TOTAL_EVENT

    # Display Results
    st.markdown("---")
    st.header("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="💉 Total First Aid Cost", value=f"RM {TOTAL_FIRST_AID}")
        st.metric(label="⚪ Total Whitezone Cost", value=f"RM {TOTAL_WHITEZONE}")

    with col2:
        st.metric(label="🎉 Total Event Cost", value=f"RM {TOTAL_EVENT}")

    st.markdown("<div class='highlighted'>💰 Pendapatan Bersih: RM {}</div>".format(PENDAPATAN_BERSIH), unsafe_allow_html=True)

elif selected == "About":
    st.header("About")
    st.write("This calculator helps doctors calculate their net income quickly and easily.")

# Display Current and Total Users
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 User Statistics")
st.sidebar.write(f"Total Users: {len(user_data['users'])}")
st.sidebar.write(f"Real-Time Users: {user_data['current_users']}")

# Remove a user when they leave the app
if st.button("Exit App"):
    remove_user()
    st.success("You have exited the app.")
