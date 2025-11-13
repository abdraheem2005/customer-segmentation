import streamlit as st
import base64
from pathlib import Path
import time

# --- Page setup ---
st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")

# --- Hide sidebar and Streamlit UI ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- Background setup ---
def set_background(image_path: str, dim: float = 0.6):
    p = Path(image_path)
    if not p.exists():
        st.warning(f"⚠️ Background image not found: {image_path}")
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
set_background("bgl.jpg", dim=0.55)


# --- Admin credentials ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

# --- Session state setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# --- Login Form ---
st.markdown("""
    <h1 style="text-align:center; color:white; font-weight:bold; text-shadow: 2px 2px 6px black;">
        🔐 Admin Login
    </h1>
""", unsafe_allow_html=True)

with st.form("login_form"):
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", placeholder="Enter password", type="password")
    login_btn = st.form_submit_button("Login")
    st.markdown("</div>", unsafe_allow_html=True)

    if login_btn:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Login successful! Redirecting to dashboard...")
            time.sleep(1.2)

            # Make navbar show immediately after login
            st.markdown("""
                <script>
                sessionStorage.removeItem("firstLoginShown");
                </script>
            """, unsafe_allow_html=True)

            st.switch_page("pages/home.py")
        else:
            st.error("❌ Invalid username or password")


# --- Auto-redirect if already logged in ---
if st.session_state.logged_in:
    st.switch_page("pages/home.py")
