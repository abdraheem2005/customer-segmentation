import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Customer Data Input", layout="centered")

# --- Safe Login State Handling ---
# If login state isn't defined, assume user just came from Home (avoid false redirect)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# --- Hide Streamlit Default UI ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Function to Set Background ---
def set_background(image_path: str, dim: float = 0.5):
    p = Path(image_path)
    if not p.exists():
        return
    with open(p, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
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

# --- Set Background ---
set_background("bgc.jpg", dim=0.5)

# --- Stylish "Back to Home" Button ---
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 8px 20px;
        color: #f5f5f5;
        font-size: 17px;
        font-weight: 500;
        border: none;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        color: #FFD700;
        background: rgba(255,255,255,0.15);
        transform: scale(1.08);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, _ = st.columns([1,1,8])
with col1:
    if st.button("🏠"):
        st.switch_page("pages/home")

# --- Page Title ---
st.markdown(
    "<h2 style='text-align:center; color:white; margin-top:20px;'>🧾 Customer Data Input</h2>",
    unsafe_allow_html=True
)

# --- Input Form ---
with st.form("customer_form"):
    col1, col2 = st.columns(2)
    with col1:
        index = st.number_input("Index", min_value=1, step=1)
        invoice_no = st.text_input("InvoiceNo (e.g., 536365)")
        stock_code = st.text_input("StockCode (e.g., 85123A)")
        description = st.text_input("Description (e.g., WHITE HANGING HEART T-LIGHT HOLDER)")
        quantity = st.number_input("Quantity", min_value=1, step=1)
    with col2:
        invoice_date = st.date_input("InvoiceDate", value=datetime.now().date())
        unit_price = st.number_input("UnitPrice", min_value=0.0, step=0.1)
        customer_id = st.text_input("CustomerID (e.g., 17850)")
        country = st.text_input("Country (e.g., United Kingdom)")

    submitted = st.form_submit_button("Submit")

# --- Display Entered Data ---
if submitted:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;'>Entered Customer Data:</h4>", unsafe_allow_html=True)

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

    st.table(df)