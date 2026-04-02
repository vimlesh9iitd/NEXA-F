import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXA — Feedback",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Google Sheets helpers ──────────────────────────────────────
COLUMNS = [
    "id", "timestamp", "name", "email", "role", "usage_duration",
    "modules_used", "overall_rating", "ease_of_use", "satisfaction",
    "best_thing", "improvement", "recommend", "feature_request",
    "message", "source",
]

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPE
    )
    client = gspread.authorize(creds)
    return client.open("NEXA_Responses").sheet1

def save_response(data: dict):
    try:
        sheet = get_sheet()
        # Agar sheet bilkul empty hai toh header row add karo
        existing = sheet.get_all_values()
        if not existing:
            sheet.append_row(COLUMNS)
        sheet.append_row([data.get(col, "") for col in COLUMNS])
    except Exception as e:
        st.error(f"❌ Response save nahi hua: {e}")
        st.stop()

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}
.stApp {
    background: linear-gradient(135deg, #080B18 0%, #0D1128 50%, #080B18 100%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 760px !important; }
.top-bar {
    position: fixed; top: 0; left: 0; right: 0; height: 3px; z-index: 999;
    background: linear-gradient(90deg, #7C6EF5, #00D4FF, #FF6B9D, #F5C842);
}
.nexa-header { text-align: center; padding: 20px 0 32px; }
.nexa-badge {
    display: inline-block; background: rgba(124,110,245,0.12);
    border: 1px solid rgba(124,110,245,0.3); border-radius: 100px;
    padding: 6px 18px; font-size: 11px; letter-spacing: 3px;
    font-weight: 700; color: #7C6EF5; text-transform: uppercase; margin-bottom: 16px;
}
.nexa-title {
    font-family: 'Syne', sans-serif !important; font-size: 2.8rem;
    font-weight: 800; margin: 0; line-height: 1.1;
    background: linear-gradient(135deg, #fff 40%, #00D4FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.nexa-sub { color: #7A85AA; font-size: 15px; margin-top: 10px; line-height: 1.6; }
.sec-header { display: flex; align-items: center; gap: 12px; margin: 28px 0 16px; }
.sec-num {
    width: 32px; height: 32px; border-radius: 8px; display: flex;
    align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 800;
    background: rgba(124,110,245,0.2); color: #7C6EF5;
}
.sec-title {
    font-family: 'Syne', sans-serif !important; font-size: 1.15rem; font-weight: 700; color: white;
}
.card {
    background: rgba(20,28,53,0.85); border: 1px solid rgba(124,110,245,0.18);
    border-radius: 18px; padding: 24px; margin-bottom: 16px;
    backdrop-filter: blur(10px);
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: rgba(8,11,24,0.9) !important;
    border: 1.5px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7C6EF5 !important;
    box-shadow: 0 0 0 3px rgba(124,110,245,0.15) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stMultiSelect label, .stSlider label, .stRadio label {
    color: #7A85AA !important; font-size: 12px !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
    font-weight: 500 !important;
}
.stRadio > div { gap: 8px !important; }
.stRadio > div > label {
    background: rgba(8,11,24,0.6) !important;
    border: 1.5px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important; padding: 8px 16px !important;
    color: #7A85AA !important; font-size: 13px !important;
    text-transform: none !important; letter-spacing: 0 !important;
    cursor: pointer !important; transition: all 0.2s !important;
}
.stRadio > div > label:has(input:checked) {
    background: rgba(124,110,245,0.15) !important;
    border-color: #7C6EF5 !important; color: white !important;
}
.stMultiSelect > div > div {
    background: rgba(8,11,24,0.9) !important;
    border: 1.5px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: rgba(124,110,245,0.2) !important;
    border-radius: 8px !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #7C6EF5, #00D4FF) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7C6EF5, #9B8AF7) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 14px 32px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 15px !important;
    font-weight: 500 !important; width: 100% !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 20px rgba(124,110,245,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,110,245,0.5) !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7C6EF5, #00D4FF) !important;
    border-radius: 100px !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 100px !important;
}
.success-box {
    text-align: center; padding: 50px 30px;
    background: rgba(20,28,53,0.85); border: 1px solid rgba(46,204,113,0.3);
    border-radius: 24px; margin: 20px 0;
}
.success-icon { font-size: 56px; margin-bottom: 16px; }
.success-title {
    font-family: 'Syne', sans-serif !important; font-size: 2rem;
    font-weight: 800; color: white; margin-bottom: 10px;
}
.success-sub { color: #7A85AA; font-size: 15px; line-height: 1.6; margin-bottom: 20px; }
.response-id {
    display: inline-block; background: rgba(124,110,245,0.1);
    border: 1px solid rgba(124,110,245,0.3); border-radius: 10px;
    padding: 8px 20px; font-size: 12px; color: #7C6EF5;
    letter-spacing: 2px; font-family: monospace;
}
.nexa-divider {
    height: 1px; background: rgba(124,110,245,0.15); margin: 8px 0 20px;
}
</style>
<div class="top-bar"></div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div class="nexa-header">
    <div class="nexa-badge">◈ NEXA PLATFORM</div>
    <div class="nexa-title">Share Your Feedback</div>
    <div class="nexa-sub">Help us shape the future of NEXA.<br>Every response is reviewed by our team.</div>
</div>
""", unsafe_allow_html=True)

# ── Session state for multi-step ──────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 1
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# ── Progress ───────────────────────────────────────────────────
TOTAL_STEPS = 4
step = st.session_state.step

if not st.session_state.submitted:
    progress = (step - 1) / TOTAL_STEPS
    st.progress(progress)
    st.caption(f"Step {step} of {TOTAL_STEPS}")

# ── SUCCESS SCREEN ─────────────────────────────────────────────
if st.session_state.submitted:
    rid = st.session_state.form_data.get("id", "")
    st.markdown(f"""
    <div class="success-box">
        <div class="success-icon">✅</div>
        <div class="success-title">Thank You! 🎉</div>
        <div class="success-sub">Your feedback has been saved.<br>The NEXA team will review it carefully.</div>
        <div class="response-id">Response ID: {rid}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Submit Another Response"):
        st.session_state.step = 1
        st.session_state.submitted = False
        st.session_state.form_data = {}
        st.rerun()
    st.stop()

fd = st.session_state.form_data

# ══════════════════════════════════════════════════════════════
# STEP 1 — About You
# ══════════════════════════════════════════════════════════════
if step == 1:
    st.markdown("""
    <div class="sec-header">
        <div class="sec-num">01</div>
        <div class="sec-title">About You</div>
    </div>
    <div class="nexa-divider"></div>
    """, unsafe_allow_html=True)

    with st.container():
        name = st.text_input("Full Name *", value=fd.get("name",""), placeholder="Enter your full name")
        email = st.text_input("Email Address *", value=fd.get("email",""), placeholder="you@example.com")
        role = st.selectbox("Role / Occupation", [
            "", "Student", "Developer / Engineer", "Researcher",
            "Healthcare Professional", "Business / Entrepreneur",
            "Content Creator", "Educator", "Other"
        ], index=["","Student","Developer / Engineer","Researcher",
                  "Healthcare Professional","Business / Entrepreneur",
                  "Content Creator","Educator","Other"].index(fd.get("role","")) if fd.get("role","") in ["","Student","Developer / Engineer","Researcher","Healthcare Professional","Business / Entrepreneur","Content Creator","Educator","Other"] else 0
        )
        duration = st.radio("How long have you used NEXA?", [
            "First time", "Less than a week", "1–4 weeks", "1–3 months", "3+ months"
        ], index=["First time","Less than a week","1–4 weeks","1–3 months","3+ months"].index(fd.get("usage_duration","First time")) if fd.get("usage_duration") else 0,
        horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue →", key="next1"):
        if not name.strip():
            st.error("⚠ Please enter your name.")
        elif "@" not in email or "." not in email:
            st.error("⚠ Please enter a valid email address.")
        else:
            fd.update({"name": name, "email": email, "role": role, "usage_duration": duration})
            st.session_state.step = 2
            st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 2 — Module Ratings
# ══════════════════════════════════════════════════════════════
elif step == 2:
    st.markdown("""
    <div class="sec-header">
        <div class="sec-num" style="background:rgba(0,212,255,0.15);color:#00D4FF">02</div>
        <div class="sec-title">Rate the Modules</div>
    </div>
    <div class="nexa-divider"></div>
    """, unsafe_allow_html=True)

    modules_default = fd.get("modules_used", "").split(", ") if fd.get("modules_used") else []
    modules = st.multiselect(
        "Which NEXA modules have you used? *",
        ["INFOCHAT", "DR. NEXA", "IMAGINE", "STUDY PLANNER",
         "YOURS NEXA", "CREATIVE", "ANALYTICS", "INDIA TOUR"],
        default=[m for m in modules_default if m],
    )

    st.markdown("<br>", unsafe_allow_html=True)
    rating = st.select_slider(
        "Overall Platform Rating *",
        options=["⭐ 1 — Poor", "⭐⭐ 2 — Below Average", "⭐⭐⭐ 3 — Average", "⭐⭐⭐⭐ 4 — Good", "⭐⭐⭐⭐⭐ 5 — Excellent"],
        value=fd.get("overall_rating", "⭐⭐⭐ 3 — Average")
    )

    ease = st.slider("Ease of Use (1 = Very Difficult, 10 = Very Easy)", 1, 10,
                     value=fd.get("ease_of_use", 5))

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Back", key="back2"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Continue →", key="next2"):
            if not modules:
                st.error("⚠ Please select at least one module.")
            else:
                fd.update({
                    "modules_used": ", ".join(modules),
                    "overall_rating": rating,
                    "ease_of_use": ease,
                })
                st.session_state.step = 3
                st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 3 — Experience
# ══════════════════════════════════════════════════════════════
elif step == 3:
    st.markdown("""
    <div class="sec-header">
        <div class="sec-num" style="background:rgba(255,107,157,0.15);color:#FF6B9D">03</div>
        <div class="sec-title">Your Experience</div>
    </div>
    <div class="nexa-divider"></div>
    """, unsafe_allow_html=True)

    satisfaction = st.radio(
        "How satisfied are you overall? *",
        ["😞 Very Dissatisfied", "😐 Dissatisfied", "🙂 Neutral", "😊 Satisfied", "🤩 Very Satisfied"],
        index=["😞 Very Dissatisfied","😐 Dissatisfied","🙂 Neutral","😊 Satisfied","🤩 Very Satisfied"].index(fd.get("satisfaction","🙂 Neutral")),
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    best = st.text_area("What's the BEST thing about NEXA?", value=fd.get("best_thing",""),
                        placeholder="What impressed you the most?", max_chars=500, height=100)
    improvement = st.text_area("What needs improvement?", value=fd.get("improvement",""),
                               placeholder="Share your honest thoughts…", max_chars=500, height=100)

    recommend = st.radio(
        "Would you recommend NEXA to others?",
        ["Definitely Yes 🙌", "Probably Yes", "Not Sure", "Probably Not", "No"],
        index=["Definitely Yes 🙌","Probably Yes","Not Sure","Probably Not","No"].index(fd.get("recommend","Probably Yes")),
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Back", key="back3"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Continue →", key="next3"):
            fd.update({
                "satisfaction": satisfaction,
                "best_thing": best,
                "improvement": improvement,
                "recommend": recommend,
            })
            st.session_state.step = 4
            st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 4 — Final Thoughts
# ══════════════════════════════════════════════════════════════
elif step == 4:
    st.markdown("""
    <div class="sec-header">
        <div class="sec-num" style="background:rgba(46,204,113,0.15);color:#2ECC71">04</div>
        <div class="sec-title">Final Thoughts</div>
    </div>
    <div class="nexa-divider"></div>
    """, unsafe_allow_html=True)

    feature_req = st.text_area(
        "What features would you like next?",
        value=fd.get("feature_request", ""),
        placeholder="New module ideas, integrations, anything…",
        max_chars=600, height=100
    )
    message = st.text_area(
        "Any other message for the NEXA team?",
        value=fd.get("message", ""),
        placeholder="Say whatever you'd like! 🚀",
        max_chars=800, height=100
    )
    source = st.selectbox(
        "How did you hear about NEXA?",
        ["", "Social Media", "Friend / Colleague", "Search Engine",
         "College / University", "Event / Hackathon", "Other"],
        index=["","Social Media","Friend / Colleague","Search Engine",
               "College / University","Event / Hackathon","Other"].index(fd.get("source","")) if fd.get("source","") in ["","Social Media","Friend / Colleague","Search Engine","College / University","Event / Hackathon","Other"] else 0
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Back", key="back4"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("✓  Submit Feedback", key="submit"):
            fd.update({
                "feature_request": feature_req,
                "message": message,
                "source": source,
                "id": "NX-" + str(uuid.uuid4())[:8].upper(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

            row = {col: fd.get(col, "") for col in COLUMNS}
            save_response(row)

            st.session_state.submitted = True
            st.rerun()
