import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase Configuration
# Initialize Firebase
cred = credentials.Certificate("pbcalc-firebase-adminsdk-fbsvc-c109c8c5fe.json")  # Path to your Firebase key file

if not firebase_admin._apps:
    try:
        firebase_admin.initialize_app(cred)
        print("Firebase app initialized!")
    except Exception as e:
        print(f"Error initializing Firebase app: {e}")

db = firestore.client()

# Firebase Functions
def add_user_to_firebase(username):
    """Add a user to the Firestore database."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.collection("users").add({"username": username, "timestamp": timestamp})
        print(f"User {username} added to Firestore successfully!")
    except Exception as e:
        print(f"Error adding user {username} to Firestore: {e}")
        st.error(f"Failed to add user {username} to the database.")

def get_users_from_firebase():
    """Retrieve all users from the Firestore database."""
    try:
        users = db.collection("users").stream()
        return [{"id": user.id, **user.to_dict()} for user in users]
    except Exception as e:
        print(f"Error retrieving users from Firestore: {e}")
        st.error("Failed to retrieve users from the database.")
        return []

def get_active_user_count():
    """Count active users (if needed for real-time updates)."""
    users = get_users_from_firebase()
    return len(users)

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
        add_user_to_firebase(username)
        st.success(f"Welcome, {username}! You are now using the app.")

# Display Active Users
users = get_users_from_firebase()

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

# Sidebar: Show User Statistics
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 User Statistics")
st.sidebar.write(f"Total Users: {len(users)}")
