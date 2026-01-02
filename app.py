import streamlit as st
from pathlib import Path
import base64
import time

from inference.predictor import predict_customer_segment

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Segmentation AI",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ============================================================
# FORCE WHITE TEXT + BLACK BUTTONS
# ============================================================
def apply_theme():
    st.markdown("""
    <style>
    /* Force all text white */
    html, body, [class*="css"] {
        color: white !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: white !important;
    }

    /* Inputs */
    input, textarea {
        color: white !important;
        background-color: #1e1e1e !important;
    }

    /* BUTTONS - BLACK */
    button {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }

    button:hover {
        background-color: #222 !important;
        color: white !important;
    }

    .stApp {
        background-color: #0e1117;
    }
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ============================================================
# BACKGROUND IMAGE
# ============================================================
def set_background(image_path: str, dim: float = 0.7):
    p = Path(image_path)
    if not p.exists():
        return

    encoded = base64.b64encode(p.read_bytes()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{encoded}") no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,{dim});
        z-index: 0;
    }}
    .block-container {{
        position: relative;
        z-index: 1;
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# NAV BAR
# ============================================================
def nav_bar():
    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
        if st.button("📊 Predict"):
            st.session_state.page = "predict"
            st.rerun()

    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

# ============================================================
# LOGIN PAGE
# ============================================================
def login_page():
    set_background("bgl.jpg", 0.4)

    st.markdown("<h1 style='text-align:center;'>🔐 Admin Login</h1>", unsafe_allow_html=True)

    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u == "admin" and p == "12345":
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.success("Login successful")
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("Invalid credentials")

# ============================================================
# HOME PAGE
# ============================================================
def home_page():
    set_background("bgh.jpg", 0.3)
    nav_bar()

    st.markdown("""
    <h1 style="text-align:center; margin-top:120px;">
        🤖 Customer Segmentation AI
    </h1>
    <p style="text-align:center;">
        Predict customer clusters using machine learning.
    </p>
    """, unsafe_allow_html=True)

# ============================================================
# PREDICTION PAGE
# ============================================================
def predict_page():
    set_background("bgc.jpg", 0.6)
    nav_bar()

    st.markdown("<h2 style='text-align:center;'>📈 Customer Segmentation Predictor</h2>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        recency = st.number_input("Recency (days)", min_value=0)
        frequency = st.number_input("Frequency", min_value=0)
        monetary = st.number_input("Monetary Value", min_value=0.0)

    with col2:
        quantity = st.number_input("Total Quantity", min_value=0)
        unique_products = st.number_input("Unique Products", min_value=0)

    if st.button("Predict Segment"):
        input_data = {
            "Recency": recency,
            "Frequency": frequency,
            "Monetary": monetary,
            "TotalQuantity": quantity,
            "UniqueProducts": unique_products
        }

        result = predict_customer_segment(input_data)

        st.success(f"KMeans Cluster: {result['kmeans_cluster']}")
        st.info(f"GMM Cluster: {result['gmm_cluster']}")
        st.write(f"GMM Confidence: {result['gmm_confidence']}")

# ============================================================
# ROUTER
# ============================================================
if not st.session_state.logged_in:
    login_page()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "predict":
    predict_page()
else:
    home_page()
