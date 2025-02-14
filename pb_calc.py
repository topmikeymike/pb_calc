import os
import streamlit as st
import math 

# Ensure required libraries are installed
os.system('pip install streamlit-option-menu')

from streamlit_option_menu import option_menu

# Set Page Configuration
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

# Title and Description
st.title("📊 Pendapatan Bersih Calculator")
st.write("Welcome! Use this tool to calculate your **Pendapatan Bersih (Net Income)** with ease and clarity.")
st.markdown("---")

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "📌 Choose Your Calculator",
        ["🩺 Calculator V1 – (If You Remember First Aid Count)", "🧮 Calculator V2 BETA – (If You Don't Remember First Aid Count)"],
        icons=["calculator", "clipboard-list"],
        menu_icon="layers",
        default_index=0,
    )


if selected == "🩺 Calculator V1 – (If You Remember First Aid Count)":
 # Input Fields
    st.header("Input Details")
    pendapatan_kasar = st.number_input("Pendapatan Kasar (Gross Income) in RM:", min_value=0, value=0, step=1)
    total_firstaid = st.number_input("Total First Aid Count:", min_value=0, value=0, step=1)
    whitezone = st.number_input("Total Whitezone Count:", min_value=0, value=0, step=1)
    event = st.number_input("Total Event Count:", min_value=0, value=0, step=1)

    # Calculations
    TOTAL_FIRST_AID = total_firstaid * 150
    TOTAL_WHITEZONE = whitezone * 50
    TOTAL_EVENT = event * 50
    PENDAPATAN_BERSIH = pendapatan_kasar - TOTAL_FIRST_AID - TOTAL_WHITEZONE - TOTAL_EVENT

    # Display Results
    st.markdown("---")
    st.header("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💉 Treatments & Costs")
        st.metric(label="💉 Total First Aid Cost", value=f"RM {TOTAL_FIRST_AID}")
        

    with col2:
        st.subheader("💼 Taxes")
        st.metric(label="⚪ Total Tax Whitezone Cost", value=f"RM {TOTAL_WHITEZONE}")
        st.metric(label="🎉 Total Tax Event Cost", value=f"RM {TOTAL_EVENT}")
        
    st.markdown("<div class='highlighted'>💰 Pendapatan Bersih: RM {}</div>".format(PENDAPATAN_BERSIH), unsafe_allow_html=True)

elif selected == "🧮 Calculator V2 BETA – (If You Don't Remember First Aid Count)":

     # Input Fields
    st.header("Input Details")
    pendapatan_kasar = st.number_input("Pendapatan Kasar (Gross Income) in RM:", min_value=0, value=0, step=1)

    # Calculate Estimated First Aid Used
    estimated_first_aid_used = round(pendapatan_kasar * 2.22 / 1000)  # Always round up
    total_first_aid_cost = estimated_first_aid_used * 150  # Each first aid costs RM200

    # Inputs for Whitezone and Event Tax
    whitezone_count = st.number_input("Enter the number of Whitezone Tax Units:", min_value=0, value=0, step=1)
    event_count = st.number_input("Enter the number of Event Tax Units:", min_value=0, value=0, step=1)

    # Calculate total whitezone and event taxes
    total_whitezone_tax = whitezone_count * 50
    total_event_tax = event_count * 50

    # Display Results
    st.markdown("---")
    st.header("Results")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💉 Treatments & Costs")
        st.metric(label="Estimated First Aid Used", value=f"{int(estimated_first_aid_used)}")
        st.metric(label="Total First Aid Cost", value=f"RM {total_first_aid_cost}")
        
    with col2:
        st.subheader("💼 Taxes")
        st.metric(label="Total Whitezone Tax", value=f"RM {total_whitezone_tax}")
        st.metric(label="Total Event Tax", value=f"RM {total_event_tax}")

    # Calculate Pendapatan Bersih (Net Income after taxes and first aid cost)
    total_tax = total_whitezone_tax + total_event_tax
    PENDAPATAN_BERSIH = pendapatan_kasar - total_first_aid_cost - total_tax

    st.markdown("<div class='highlighted'>💰 Pendapatan Bersih: RM {}</div>".format(int(PENDAPATAN_BERSIH)), unsafe_allow_html=True)

