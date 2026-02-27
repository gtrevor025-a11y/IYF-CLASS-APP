import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. MOBILE-FIRST SETTINGS ---
st.set_page_config(page_title="IYF AI Hub", layout="centered")

# Welcome Animation
if "first_load" not in st.session_state:
    st.balloons()
    st.toast("Welcome to IYF AI & Data Science Class! 🚀")
    st.session_state.first_load = True

# Custom CSS for Mobile Navigation & Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { width: 100%; height: 50px; border-radius: 12px; font-size: 18px !important; }
    .fixed-footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #111; display: flex; justify-content: space-around;
        padding: 10px 0; border-top: 1px solid #333; z-index: 999;
    }
    .main .block-container { padding-bottom: 100px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE GOOGLE SHEETS CONNECTION ---
# Your specific link integrated here:
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yvlawElm0BbzaQsrnTxRT10W2yi04YesPWv9_mLSBuU/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # This reads your specific sheet link directly
    return conn.read(spreadsheet=SHEET_URL, ttl="1m")

# --- 3. NAVIGATION LOGIC ---
if "page" not in st.session_state: st.session_state.page = "Feed"

# Bottom Nav Bar (Mobile Friendly)
st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
if c1.button("🏠"): st.session_state.page = "Feed"
if c2.button("➕"): st.session_state.page = "Post"
if c3.button("🎥"): st.session_state.page = "Live"
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PAGE ROUTING ---

# FEED PAGE
if st.session_state.page == "Feed":
    st.title("🌐 Class Feed")
    try:
        df = get_data()
        if df.empty:
            st.info("No posts yet. Be the first to share!")
        else:
            # Show newest posts at the top
            for index, row in df.iloc[::-1].iterrows():
                with st.container(border=True):
                    st.markdown(f"**👤 {row.get('user', 'Guest')}** | `{row.get('topic', 'General')}`")
                    st.caption(f"🕒 {row.get('time', '')}")
                    st.write(row.get('content', ''))
                    if pd.notna(row.get('code')) and row.get('code') != "":
                        st.code(row['code'], language="python")
    except Exception as e:
        st.error(f"Connection Error: Ensure your Google Sheet 'Share' settings are set to 'Anyone with the link can EDIT'.")

# POST PAGE
elif st.session_state.page == "Post":
    st.title("➕ Create Post")
    with st.form("post_form", clear_on_submit=True):
        u_name = st.text_input("Your Name", placeholder="e.g. Kelvin")
        u_topic = st.selectbox("Topic", ["Python", "Data Science", "AI", "General"])
        u_msg = st.text_area("Message", placeholder="What did you learn today?")
        u_code = st