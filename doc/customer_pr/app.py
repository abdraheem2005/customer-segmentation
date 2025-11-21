import streamlit as st
from pathlib import Path
import base64
import pandas as pd
from datetime import datetime
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Customer Segmentation AI", page_icon="🤖", layout="wide")

# Hide default streamlit UI
HIDE_UI = """
<style>
[data-testid="stSidebar"] {display: none;}
#MainMenu, footer, header {visibility: hidden;}
</style>
"""
st.markdown(HIDE_UI, unsafe_allow_html=True)

# ============================================================
# BACKGROUND FUNCTION (reusable)
# ============================================================
def set_background(image_path: str, dim: float = 0.5):
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
# LOGIN PAGE
# ============================================================
def login_page():
    set_background("bgl.jpg", dim=0.55)

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "12345"

    st.markdown("""
        <h1 style="text-align:center; color:white; text-shadow: 2px 2px 6px black;">
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
                time.sleep(1)
            else:
                st.error("Invalid username or password")


# ============================================================
# NAVIGATION BAR
# ============================================================
def navigation_bar():
    st.markdown("""
        <style>
        .topnav {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border-radius: 18px;
            padding: 8px 20px;
            display: flex;
            justify-content: space-between;
            z-index: 9999;
        }
        .topnav a {
            color: #fff;
            font-size: 18px;
            font-weight: 500;
            text-decoration: none;
            margin: 0 10px;
        }
        .logout-btn {
            background: #ff4b4b;
            padding: 8px 20px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4,1])
    with col1:
        st.write(
            '<div class="topnav">'
            '<a href="#" onclick="window.location.href=\'?page=home\'">🏠 Home</a>'
            '<a href="#" onclick="window.location.href=\'?page=input\'">📊 Data Input</a>'
            '</div>',
            unsafe_allow_html=True
        )
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.success("Logged out!")
            time.sleep(1)


# ============================================================
# HOME PAGE
# ============================================================
def home_page():
    set_background("bgh.jpg", dim=0.4)

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
    set_background("bgc.jpg", dim=0.5)
    navigation_bar()

    st.markdown("<h2 style='text-align:center; color:white;'>🧾 Customer Data Input</h2>", unsafe_allow_html=True)

    with st.form("customer_form"):
        col1, col2 = st.columns(2)
        with col1:
            index = st.number_input("Index", min_value=1)
            invoice_no = st.text_input("InvoiceNo")
            stock_code = st.text_input("StockCode")
            description = st.text_input("Description")
            quantity = st.number_input("Quantity", min_value=1)
        with col2:
            invoice_date = st.date_input("InvoiceDate", value=datetime.now().date())
            unit_price = st.number_input("UnitPrice", min_value=0.0)
            customer_id = st.text_input("CustomerID")
            country = st.text_input("Country")

        submitted = st.form_submit_button("Submit")

    if submitted:
        df = pd.DataFrame({
            "Index": [index],
            "InvoiceNo": [invoice_no],
            "StockCode": [stock_code],
            "Description": [description],
            "Quantity": [quantity],
            "InvoiceDate": [invoice_date],
            "UnitPrice": [unit_price],
            "CustomerID": [customer_id],
            "Country": [country]
        })
        st.success("Data Submitted Successfully")
        st.table(df)


# ============================================================
# ROUTER (Single Entry Point)
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

query = st.query_params.get("page")
if query:
    st.session_state.page = query[0]

# --- Page Routing ---
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "input":
        input_page()
    else:
        home_page()
