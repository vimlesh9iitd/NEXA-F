import streamlit as st
import pandas as pd
import io
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="NEXA — Admin Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auth ───────────────────────────────────────────────────────
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "nexa2024")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&family=DM+Sans:wght@400;500&display=swap');
    html,[class*="css"]{font-family:'DM Sans',sans-serif!important}
    .stApp{background:#080B18}
    #MainMenu,footer,header{visibility:hidden}
    .block-container{max-width:400px!important;padding-top:5rem!important}
    .stTextInput>div>div>input{background:rgba(20,28,53,0.9)!important;border:1.5px solid rgba(124,110,245,0.3)!important;border-radius:12px!important;color:white!important}
    .stButton>button{background:linear-gradient(135deg,#7C6EF5,#9B8AF7)!important;color:white!important;border:none!important;border-radius:12px!important;width:100%!important;padding:14px!important;font-size:15px!important}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='font-family:Syne,sans-serif;color:white;text-align:center;margin-bottom:8px'>◈ NEXA Admin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7A85AA;text-align:center;margin-bottom:28px'>Enter password to access dashboard</p>", unsafe_allow_html=True)

    pwd = st.text_input("Password", type="password", placeholder="Enter admin password")
    if st.button("Login →"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,[class*="css"]{font-family:'DM Sans',sans-serif!important}
.stApp{background:#080B18}
#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:#0F1526!important;border-right:1px solid rgba(124,110,245,0.18)!important}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#7A85AA}

/* Metric cards */
[data-testid="stMetric"]{
    background:rgba(20,28,53,0.85);border:1px solid rgba(124,110,245,0.18);
    border-radius:16px;padding:20px!important;
}
[data-testid="stMetricLabel"]{color:#7A85AA!important;font-size:12px!important;text-transform:uppercase;letter-spacing:1px}
[data-testid="stMetricValue"]{color:white!important;font-family:'Syne',sans-serif!important;font-size:2rem!important}

/* Dataframe */
[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,0.04);border-radius:12px;padding:4px;gap:4px}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;color:#7A85AA!important;background:transparent!important}
.stTabs [aria-selected="true"]{background:rgba(124,110,245,0.2)!important;color:white!important}

/* Buttons */
.stButton>button{background:linear-gradient(135deg,#7C6EF5,#9B8AF7)!important;color:white!important;border:none!important;border-radius:10px!important;font-family:'DM Sans',sans-serif!important}
.stDownloadButton>button{background:rgba(46,204,113,0.15)!important;color:#2ECC71!important;border:1px solid rgba(46,204,113,0.3)!important;border-radius:10px!important}

/* Top accent */
.top-bar{position:fixed;top:0;left:0;right:0;height:3px;z-index:999;background:linear-gradient(90deg,#7C6EF5,#00D4FF,#FF6B9D,#F5C842)}

.stat-label{font-size:11px;color:#7A85AA;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.big-num{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:white;line-height:1}
.sub-text{font-size:12px;color:#7A85AA;margin-top:4px}

.section-head{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:white;margin:20px 0 12px}

.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.bar-label-text{font-size:13px;color:#cbd5e1;min-width:130px}
.bar-track{flex:1;background:rgba(255,255,255,0.06);border-radius:100px;height:8px;overflow:hidden}
.bar-count{font-size:12px;color:#7A85AA;min-width:24px;text-align:right}
</style>
<div class="top-bar"></div>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────
DATA_FILE = Path("data/responses.csv")

COLUMNS = [
    "id", "timestamp", "name", "email", "role", "usage_duration",
    "modules_used", "overall_rating", "ease_of_use", "satisfaction",
    "best_thing", "improvement", "recommend", "feature_request",
    "message", "source",
]

@st.cache_data(ttl=10)
def load_data():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(DATA_FILE)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='font-family:Syne,sans-serif;color:white;margin-bottom:4px'>◈ NEXA Admin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7A85AA;font-size:12px;margin-bottom:20px'>Feedback Dashboard</p>", unsafe_allow_html=True)
    st.divider()

    if st.button("🔄  Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.markdown("<p style='color:#7A85AA;font-size:12px'>Admin v1.0 · NEXA Platform</p>", unsafe_allow_html=True)

    if st.button("🚪  Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ── Main ───────────────────────────────────────────────────────
df = load_data()
n = len(df)

st.markdown("<h1 style='font-family:Syne,sans-serif;color:white;margin-bottom:4px'>📋 Feedback Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#7A85AA;margin-bottom:24px'>{n} total responses collected</p>", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Responses", n)
with c2:
    if n:
        # Extract numeric rating
        def parse_rating(r):
            try: return int(str(r)[0])
            except: return 0
        avg_r = df["overall_rating"].apply(parse_rating).mean()
        st.metric("Avg Rating", f"{avg_r:.1f} ★")
    else:
        st.metric("Avg Rating", "—")
with c3:
    if n:
        rec = df["recommend"].str.contains("Yes", na=False).sum()
        st.metric("Would Recommend", f"{int(rec/n*100)}%")
    else:
        st.metric("Would Recommend", "—")
with c4:
    if n:
        avg_e = pd.to_numeric(df["ease_of_use"], errors="coerce").mean()
        st.metric("Avg Ease Score", f"{avg_e:.1f}/10")
    else:
        st.metric("Avg Ease Score", "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋  All Responses", "📊  Analytics", "💾  Export"])

# ─────────────────────────────────────────────────────────────
with tab1:
    if n == 0:
        st.info("No responses yet. Share the feedback form to start collecting!")
    else:
        search = st.text_input("🔍  Search by name, email, module…", placeholder="Type to filter…")
        filtered = df.copy()
        if search:
            mask = df.apply(lambda row: search.lower() in row.to_string().lower(), axis=1)
            filtered = df[mask]

        st.markdown(f"<p style='color:#7A85AA;font-size:13px'>{len(filtered)} result(s)</p>", unsafe_allow_html=True)

        # Display table
        display_cols = ["id","timestamp","name","email","role","overall_rating","satisfaction","recommend"]
        st.dataframe(
            filtered[display_cols].rename(columns={
                "id":"ID","timestamp":"Date","name":"Name","email":"Email",
                "role":"Role","overall_rating":"Rating","satisfaction":"Satisfaction","recommend":"Recommend"
            }),
            use_container_width=True, hide_index=True,
        )

        st.markdown("---")
        st.markdown("<div class='section-head'>🔍 View Individual Response</div>", unsafe_allow_html=True)

        ids = filtered["id"].dropna().tolist()
        if ids:
            selected_id = st.selectbox("Select Response ID", ids)
            row = filtered[filtered["id"] == selected_id].iloc[0]

            c1, c2 = st.columns(2)
            fields_left = [("Name", "name"), ("Email", "email"), ("Role", "role"),
                           ("Usage Duration", "usage_duration"), ("Rating", "overall_rating"),
                           ("Ease of Use", "ease_of_use"), ("Source", "source"), ("Timestamp", "timestamp")]
            fields_right = [("Satisfaction", "satisfaction"), ("Recommend", "recommend"),
                            ("Modules Used", "modules_used"), ("Best Thing", "best_thing"),
                            ("Improvement", "improvement"), ("Feature Request", "feature_request"),
                            ("Message", "message")]

            with c1:
                for label, col in fields_left:
                    st.markdown(f"<div style='margin-bottom:12px'><div style='font-size:11px;color:#7A85AA;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px'>{label}</div><div style='color:white;font-size:14px;font-weight:500'>{row.get(col,'—') or '—'}</div></div>", unsafe_allow_html=True)
            with c2:
                for label, col in fields_right:
                    val = str(row.get(col, "") or "—")
                    is_long = len(val) > 60
                    style = "color:rgba(255,255,255,0.8);font-size:13px;line-height:1.6" if is_long else "color:white;font-size:14px;font-weight:500"
                    st.markdown(f"<div style='margin-bottom:12px'><div style='font-size:11px;color:#7A85AA;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px'>{label}</div><div style='{style}'>{val}</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
with tab2:
    if n == 0:
        st.info("No data yet to analyse.")
    else:
        def bar_chart(title, counts_dict, color="#7C6EF5"):
            st.markdown(f"<div class='section-head'>{title}</div>", unsafe_allow_html=True)
            if not counts_dict:
                st.caption("No data")
                return
            max_v = max(counts_dict.values()) or 1
            for label, count in sorted(counts_dict.items(), key=lambda x: -x[1]):
                pct = count / max_v * 100
                st.markdown(f"""
                <div class="bar-row">
                    <div class="bar-label-text">{label}</div>
                    <div class="bar-track"><div style="height:100%;width:{pct}%;background:{color};border-radius:100px;transition:width 0.8s"></div></div>
                    <div class="bar-count">{count}</div>
                </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Ratings
            def parse_rating(r):
                try: return int(str(r)[0])
                except: return None
            rating_counts = df["overall_rating"].apply(parse_rating).value_counts().to_dict()
            rating_display = {f"{'★'*k} ({k}/5)": v for k, v in sorted(rating_counts.items()) if k}
            bar_chart("⭐ Star Ratings", rating_display, "#F5C842")

            st.markdown("<br>", unsafe_allow_html=True)

            # Roles
            role_counts = df["role"].fillna("Not specified").replace("","Not specified").value_counts().to_dict()
            bar_chart("👥 User Roles", role_counts, "#7C6EF5")

        with col2:
            # Satisfaction
            sat_counts = df["satisfaction"].fillna("Not specified").replace("","Not specified").value_counts().to_dict()
            bar_chart("😊 Satisfaction", sat_counts, "#2ECC71")

            st.markdown("<br>", unsafe_allow_html=True)

            # Modules
            all_modules = []
            for cell in df["modules_used"].dropna():
                all_modules.extend([m.strip() for m in str(cell).split(",") if m.strip()])
            mod_counts = pd.Series(all_modules).value_counts().to_dict()
            bar_chart("🧩 Most Used Modules", mod_counts, "#00D4FF")

        st.markdown("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            rec_counts = df["recommend"].fillna("Not answered").replace("","Not answered").value_counts().to_dict()
            bar_chart("🙌 Would Recommend?", rec_counts, "#FF6B9D")
        with col4:
            src_counts = df["source"].fillna("Not specified").replace("","Not specified").value_counts().to_dict()
            bar_chart("📣 Discovery Source", src_counts, "#FF8C42")

# ─────────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-head'>💾 Export All Responses</div>", unsafe_allow_html=True)

    if n == 0:
        st.info("No responses to export yet.")
    else:
        st.markdown(f"<p style='color:#7A85AA;font-size:14px;margin-bottom:20px'>{n} responses ready to export.</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                "📊  Download CSV (Excel)",
                data=csv_buffer.getvalue(),
                file_name=f"nexa_feedback_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col2:
            st.download_button(
                "🗂  Download JSON",
                data=df.to_json(orient="records", indent=2),
                file_name=f"nexa_feedback_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-head'>📂 Import Responses</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#7A85AA;font-size:13px;margin-bottom:12px'>Merge responses from another export (CSV or JSON).</p>", unsafe_allow_html=True)

        uploaded = st.file_uploader("Upload CSV or JSON", type=["csv", "json"])
        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    imported_df = pd.read_csv(uploaded)
                else:
                    imported_df = pd.read_json(uploaded)

                existing_ids = set(df["id"].dropna().tolist())
                new_rows = imported_df[~imported_df["id"].isin(existing_ids)]

                if len(new_rows):
                    combined = pd.concat([df, new_rows], ignore_index=True)
                    combined.to_csv(DATA_FILE, index=False)
                    st.cache_data.clear()
                    st.success(f"✅ Imported {len(new_rows)} new responses ({len(imported_df)-len(new_rows)} duplicates skipped).")
                    st.rerun()
                else:
                    st.warning("All responses in this file already exist.")
            except Exception as e:
                st.error(f"Failed to import: {e}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-head' style='color:#FF6B9D'>⚠ Danger Zone</div>", unsafe_allow_html=True)
        with st.expander("Delete all responses"):
            st.warning(f"This will permanently delete all {n} responses. Export first!")
            confirm = st.text_input("Type DELETE to confirm")
            if st.button("🗑  Delete All Responses") and confirm == "DELETE":
                pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)
                st.cache_data.clear()
                st.success("All responses deleted.")
                st.rerun()
