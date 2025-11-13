import streamlit as st
import base64
from pathlib import Path
import time

# --- Page setup ---
st.set_page_config(page_title="Customer Segmentation AI", page_icon="🤖", layout="wide")

# --- Hide Streamlit UI elements ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- Background setup ---
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
        background-color: rgba(0, 0, 0, {dim});
        z-index: 0;
    }}
    .block-container {{
        position: relative;
        z-index: 1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --- Apply background ---
set_background("bgh.jpg", dim=0.4)


# --- Protect page (login check) ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first.")
    time.sleep(1.2)
    st.switch_page("login.py")


# --- Modern Glassy Navigation Bar ---
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
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        overflow: hidden;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 20px;
        transition: all 0.4s ease-in-out;
        opacity: 1;
        z-index: 9999;
    }
    .topnav:hover {
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 6px 25px rgba(255, 255, 255, 0.2);
        opacity: 1;
    }
    .topnav a {
        color: #f5f5f5;
        text-decoration: none;
        font-size: 18px;
        font-weight: 500;
        margin: 0 10px;
        letter-spacing: 0.6px;
        transition: color 0.3s ease, transform 0.3s ease;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
    }
    .topnav a:hover {
        color: #FFD700;
        transform: scale(1.08);
    }
    .logout-btn {
        background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
        padding: 10px 20px;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 2px 10px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
    }
    .logout-btn:hover {
        background: linear-gradient(90deg, #ff6b6b, #ff4b4b);
        transform: scale(1.05);
    }
    </style>

    <div class="topnav">
      <div>
        <a href="/home" target="_self">🏠 Home</a>
        <a href="/customer_input" target="_self">📊 Data Input</a>
        <a href="/pages/aa" target="_self">📈 Example 1</a>
        <a href="/pages/example2" target="_self">🧩 Example 2</a>
      </div>
      <a href="?logout=true" class="logout-btn">🚪 Logout</a>
    </div>
""", unsafe_allow_html=True)


# --- Logout redirect ---
params = st.query_params
if params.get("logout") == "true":
    st.session_state.logged_in = False
    st.success("✅ Logging out...")
    time.sleep(1)
    st.switch_page("login.py")


# --- Main Title ---
st.markdown("""
    <h1 style="
        text-align:center;
        font-size:60px;
        color:white;
        font-weight:700;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 1px;
        text-shadow: 3px 3px 12px rgba(0,0,0,0.8);
        margin-top: 120px;
    ">
        🤖 Customer Segmentation AI
    </h1>
""", unsafe_allow_html=True)

# --- Subtitle ---
st.markdown("""
    <p style="text-align:center; font-size:22px; color:#f0f0f0; margin-top:10px; font-weight:400;">
        Welcome to the AI-powered Customer Segmentation System.<br>
        <span style="opacity:0.9;">Analyze, classify, and understand your customers better with data-driven insights.</span>
    </p>
""", unsafe_allow_html=True)
