import streamlit as st
from pathlib import Path
import base64
import pandas as pd
from datetime import datetime
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Segmentation AI",
    page_icon="🤖",
    layout="wide"
)

# Hide default Streamlit UI
HIDE_UI = """
<style>
[data-testid="stSidebar"] {display: none;}
#MainMenu, footer, header {visibility: hidden;}
</style>
"""
st.markdown(HIDE_UI, unsafe_allow_html=True)

# ============================================================
# BACKGROUND FUNCTION
# ============================================================
def set_background(image_path: str, dim: float = 1.0):
    p = Path(image_path)
    if not p.exists():
        return
    encoded = base64.b64encode(p.read_bytes()).decode()
    css = f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{encoded}") no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background-color: rgba(0,0,0,{dim});
        z-index: 0;
    }}
    .block-container {{
        position: relative;
        z-index: 1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================
# INIT SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "customer_data" not in st.session_state:
    st.session_state.customer_data = pd.DataFrame(
        columns=[
            "Index", "InvoiceNo", "StockCode", "Description",
            "Quantity", "InvoiceDate", "UnitPrice",
            "CustomerID", "Country"
        ]
    )

# ============================================================
# LOGIN PAGE
# ============================================================
def login_page():
    set_background("bgl.jpg", dim=0)

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "12345"

    st.markdown("""
        <h1 style="text-align:center; color:white; text-shadow:2px 2px 6px black;">
            🔐 Admin Login
        </h1>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.success("Login successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid username or password")

# ============================================================
# NAVIGATION BAR
# ============================================================
def navigation_bar():
    col1, col2 = st.columns([4,1])

    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()

        if st.button("📊 Data Input"):
            st.session_state.page = "input"
            st.rerun()

    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

# ============================================================
# HOME PAGE
# ============================================================
def home_page():
    set_background("bgh.jpg", dim=0.3)
    navigation_bar()

    st.markdown("""
        <h1 style="text-align:center; color:white; margin-top:120px;">
            🤖 Customer Segmentation AI
        </h1>
        <p style="text-align:center; color:#f0f0f0;">
            Analyze and understand customer clusters with machine learning.
        </p>
    """, unsafe_allow_html=True)

# ============================================================
# INPUT PAGE
# ============================================================
def input_page():
    set_background("bgc.jpg", dim=0.8)
    navigation_bar()

    st.markdown(
        "<h2 style='text-align:center; color:white;'>🧾 Customer Data Input</h2>",
        unsafe_allow_html=True
    )

    with st.form("customer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            index = st.number_input("Index", min_value=1)
            invoice_no = st.text_input("InvoiceNo")
            stock_code = st.text_input("StockCode")
            description = st.text_input("Description")
            quantity = st.number_input("Quantity", min_value=1)

        with col2:
            invoice_date = st.date_input("InvoiceDate")
            unit_price = st.number_input("UnitPrice", min_value=0.0)
            customer_id = st.text_input("CustomerID")
            country = st.text_input("Country")

        submitted = st.form_submit_button("Submit")

    if submitted:
        # Append new row to session_state DataFrame
        new_row = {
            "Index": index,
            "InvoiceNo": invoice_no,
            "StockCode": stock_code,
            "Description": description,
            "Quantity": quantity,
            "InvoiceDate": invoice_date,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Country": country
        }

        st.session_state.customer_data = pd.concat(
            [st.session_state.customer_data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        st.success("Data saved successfully!")

    # Show all submitted rows in a table
    if not st.session_state.customer_data.empty:
        st.subheader("📋 All Submitted Customer Data")
        st.dataframe(st.session_state.customer_data, use_container_width=True)

# ============================================================
# APP ROUTER
# ============================================================
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "input":
        input_page()
    else:
        home_page()
#new