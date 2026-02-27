import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="IYF AI Hub", layout="centered")

# Use your "Publish to Web" CSV link here
CSV_URL = "https://docs.google.com/spreadsheets/d/1yvlawElm0BbzaQsrnTxRT10W2yi04YesPWv9_mLSBuU/export?format=csv"

# Use your Google Form "Send" link here
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfYourFormID/viewform?embedded=true"

# --- 2. MOBILE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .fixed-footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #111; display: flex; justify-content: space-around;
        padding: 15px 0; border-top: 2px solid #333; z-index: 999;
    }
    .main .block-container { padding-bottom: 110px; }
    .post-card { border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 10px; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVIGATION ---
if "page" not in st.session_state: st.session_state.page = "Feed"

st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
if c1.button("🏠 Feed"): st.session_state.page = "Feed"
if c2.button("➕ Post"): st.session_state.page = "Post"
if c3.button("🎥 Live"): st.session_state.page = "Live"
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PAGES ---

if st.session_state.page == "Feed":
    st.title("🌐 Class Feed")
    try:
        df = pd.read_csv(CSV_URL)
        # Note: Columns depend on your Form question order
        # Usually: 0=Time, 1=Name, 2=PFP_URL, 3=Content, 4=Media_URL, 5=Code
        for index, row in df.iloc[::-1].iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([1, 4])
                
                # Profile Picture (if column 2 has a link)
                pfp = row.iloc[2] if pd.notna(row.iloc[2]) else "https://cdn-icons-png.flaticon.com/512/149/149071.png"
                col1.image(pfp, width=50)
                col2.markdown(f"**{row.iloc[1]}**")
                
                # Content
                st.write(row.iloc[3])
                
                # Image/Video Media (if column 4 has a link)
                if pd.notna(row.iloc[4]) and "http" in str(row.iloc[4]):
                    media_url = str(row.iloc[4])
                    if any(x in media_url for x in [".mp4", "youtube", "vimeo"]):
                        st.video(media_url)
                    else:
                        st.image(media_url, use_container_width=True)
                
                # Code
                if len(row) > 5 and pd.notna(row.iloc[5]):
                    st.code(row.iloc[5])
    except:
        st.info("Feed is loading... make sure you 'Published to Web' as CSV in Google Sheets!")

elif st.session_state.page == "Post":
    st.title("➕ New Post")
    st.info("Tip: To show a photo, upload it to a site like postimages.org and paste the 'Direct Link' in the Media box!")
    components.html(f'<iframe src="{FORM_URL}" width="100%" height="800" frameborder="0">Loading…</iframe>', height=820)

elif st.session_state.page == "Live":
    st.title("📹 Live Meeting")
    components.html('<iframe src="https://meet.jit.si/IYF_AI_Hub_2026" allow="camera; microphone; fullscreen" style="height: 500px; width: 100%; border:none;"></iframe>', height=520)
