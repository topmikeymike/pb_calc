import os
import streamlit as st

# Ensure required libraries are installed
os.system('pip install streamlit-option-menu')

from streamlit_option_menu import option_menu

# Set Page Configuration
st.set_page_config(page_title="PENDAPATAN BERSIH CALCULATOR", page_icon="📊", layout="centered")

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

# Title and Description
st.title("📊 PENDAPATAN BERSIH CALCULATOR")
st.write("Welcome! Use this tool to calculate your **Pendapatan Bersih (Net Income)** with ease and clarity.")
st.markdown("---")

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home", "About"],
        icons=["house", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
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
        st.metric(label="⚪ Total Tax Whitezone Cost", value=f"RM {TOTAL_WHITEZONE}")

    with col2:
        st.metric(label="🎉 Total Tax Event Cost", value=f"RM {TOTAL_EVENT}")

    st.markdown("<div class='highlighted'>💰 Pendapatan Bersih: RM {}</div>".format(PENDAPATAN_BERSIH), unsafe_allow_html=True)

elif selected == "About":
    st.header("About")
    st.write("This calculator to help doctor to calculate their net-income fast and easy huhu ")
