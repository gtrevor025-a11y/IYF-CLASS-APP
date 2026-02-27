import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="IYF AI Hub", layout="centered")

# Custom CSS for Mobile Navigation & Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { 
        width: 100%; 
        height: 55px; 
        border-radius: 15px; 
        font-size: 18px !important; 
        font-weight: bold;
    }
    /* Fixed Bottom Navigation Bar */
    .fixed-footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #111; display: flex; justify-content: space-around;
        padding: 15px 0; border-top: 2px solid #333; z-index: 999;
    }
    /* Prevents content from being hidden by the footer */
    .main .block-container { padding-bottom: 130px; }
    
    /* Post Cards styling */
    .post-container {
        border: 1px solid #333;
        border-radius: 15px;
        padding: 15px;
        background-color: #111;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
# Using your specific Google Sheet link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yvlawElm0BbzaQsrnTxRT10W2yi04YesPWv9_mLSBuU/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. STATE MANAGEMENT ---
if "page" not in st.session_state: st.session_state.page = "Feed"
if "chat_target" not in st.session_state: st.session_state.chat_target = None
if "welcomed" not in st.session_state:
    st.balloons()
    st.session_state.welcomed = True

# --- 4. BOTTOM NAVIGATION MENU (For Mobile Thumbs) ---
st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🏠"): st.session_state.page = "Feed"
with c2:
    if st.button("➕"): st.session_state.page = "Post"
with c3:
    if st.button("💬"): st.session_state.page = "Chat"
with c4:
    if st.button("🎥"): st.session_state.page = "Live"
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE ROUTING ---

# PAGE: FEED (The main activity stream)
if st.session_state.page == "Feed":
    st.title("🌐 Class Feed")
    try:
        # Read data from Google Sheets
        df = conn.read(spreadsheet=SHEET_URL, ttl="1m")
        
        if df.empty:
            st.info("The feed is quiet... Tap ➕ to start the conversation!")
        else:
            # Show the latest posts at the top
            for index, row in df.iloc[::-1].iterrows():
                with st.container(border=True):
                    # Header: Name and Chat Button
                    head1, head2 = st.columns([4, 1])
                    user_name = row.get('user', 'Guest')
                    head1.markdown(f"### 👤 {user_name}")
                    
                    # If they tap the chat button, switch to Chat page
                    if head2.button("💬", key=f"chat_{index}"):
                        st.session_state.chat_target = user_name
                        st.session_state.page = "Chat"
                        st.rerun()
                    
                    st.caption(f"🕒 {row.get('time', '')} | 📚 {row.get('topic', 'General')}")
                    st.write(row.get('content', ''))
                    
                    # Display Code Snippet if it exists
                    if pd.notna(row.get('code')) and row.get('code').strip() != "":
                        st.code(row['code'], language="python")
    except Exception as e:
        st.error("Connection error. Make sure your Google Sheet is Shared as 'Editor'.")

# PAGE: POST (Simplified creation screen)
elif st.session_state.page == "Post":
    st.title("➕ Create Post")
    
    u_name = st.text_input("👤 Your Name", placeholder="Kelvin...")
    u_topic = st.selectbox("📚 Topic", ["Python Basics", "Data Science", "AI Chat", "General"])
    u_msg = st.text_area("📝 Message", placeholder="What's on your mind?", height=120)
    u_code = st.text_area("💻 Python Code (Optional)", placeholder="Paste code here...")
    
    st.markdown("---")
    
    # BIG SUBMIT BUTTON (No form used to ensure visibility)
    if st.button("🚀 PUBLISH TO FEED", use_container_width=True):
        if u_msg.strip() == "" and u_code.strip() == "":
            st.warning("Please add some text or code before posting!")
        else:
            with st.spinner("Sharing with class..."):
                # Create the new row
                new_row = pd.DataFrame([{
                    "user": u_name if u_name else "Guest",
                    "topic": u_topic,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "content": u_msg,
                    "code": u_code
                }])
                
                # Fetch existing data, add new row, and update Sheet
                existing_df = conn.read(spreadsheet=SHEET_URL)
                updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                conn.update(spreadsheet=SHEET_URL, data=updated_df)
                
                st.success("✅ Successfully Posted!")
                st.session_state.page = "Feed"
                st.rerun()

# PAGE: CHAT (Private communication)
elif st.session_state.page == "Chat":
    target = st.session_state.chat_target if st.session_state.chat_target else "Classmate"
    st.title(f"💬 Chatting with {target}")
    
    # Mock chat interface
    st.chat_message("assistant").write(f"This is your private space with {target}. Start typing below!")
    
    chat_msg = st.chat_input(f"Send a message to {target}...")
    if chat_msg:
        st.success(f"Message sent to {target}!")

# PAGE: LIVE (Jitsi Meeting)
elif st.session_state.page == "Live":
    st.title("📹 Live Classroom")
    st.write("Join the class meeting below:")
    
    # Embed Jitsi Meet
    components.html(
        f"""
        <iframe src="https://meet.jit.si/IYF_AI_Hub_Class_2026" 
        allow="camera; microphone; fullscreen; display-capture" 
        style="height: 550px; width: 100%; border-radius: 20px; border:none;"></iframe>
        """, height=560
    )
