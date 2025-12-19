import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Social Media Analytics Pro",
    page_icon="🚀",
    layout="wide"
)

# =================================================
# ADVANCED CSS + ANIMATIONS
# =================================================
st.markdown("""
<style>

/* -------- Global Background -------- */
.main {
    background: linear-gradient(to right, #141E30, #243B55);
    animation: fadeIn 1.2s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* -------- Animated Gradient Text -------- */
.gradient-text {
    background: linear-gradient(90deg,#00c6ff,#0072ff,#7f00ff,#e100ff);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 6s infinite linear;
}

@keyframes gradientMove {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}

/* -------- KPI Cards -------- */
.metric-card {
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.4);
    animation: slideUp 0.8s ease forwards;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0px 12px 40px rgba(0,0,0,0.6);
}

.blue { background: linear-gradient(135deg,#396afc,#2948ff); }
.green { background: linear-gradient(135deg,#11998e,#38ef7d); }
.orange { background: linear-gradient(135deg,#f7971e,#ffd200); }
.red { background: linear-gradient(135deg,#ff416c,#ff4b2b); }
.purple { background: linear-gradient(135deg,#667eea,#764ba2); }

@keyframes slideUp {
    from { transform: translateY(40px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* -------- Glow & Pulse -------- */
.glow {
    animation: glowPulse 2.5s infinite alternate;
}

@keyframes glowPulse {
    from { box-shadow: 0 0 10px rgba(102,126,234,0.4); }
    to { box-shadow: 0 0 25px rgba(118,75,162,0.9); }
}

/* -------- Section Animation -------- */
.section {
    animation: sectionFade 1s ease forwards;
    margin-top: 30px;
}

@keyframes sectionFade {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
}

/* -------- Progress Bar -------- */
.progress-bar {
    height: 12px;
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg,#38ef7d,#11998e);
    animation: progressGrow 1.5s ease-out;
}

@keyframes progressGrow {
    from { width: 0%; }
    to { width: 100%; }
}

</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# =================================================
# DERIVED METRICS
# =================================================
df["revenue_generated"] = df["ad_spend"] * (1 + df["roi"])

# =================================================
# SIDEBAR FILTERS
# =================================================
st.sidebar.markdown("## 🎛️ Dashboard Controls")

platform_filter = st.sidebar.multiselect(
    "📱 Platform", df["platform"].unique(), df["platform"].unique()
)
content_filter = st.sidebar.multiselect(
    "🖼️ Content Type", df["content_type"].unique(), df["content_type"].unique()
)
year_filter = st.sidebar.multiselect(
    "📅 Year", df["year"].unique(), df["year"].unique()
)

filtered_df = df[
    (df["platform"].isin(platform_filter)) &
    (df["content_type"].isin(content_filter)) &
    (df["year"].isin(year_filter))
]

# =================================================
# HEADER
# =================================================
st.markdown("""
<h1 class="gradient-text" style="text-align:center;">
🚀 Social Media Analytics Pro Dashboard
</h1>
<p style="text-align:center;color:#dcdcdc;font-size:18px;">
Engagement • Content • Campaign ROI • Revenue • Best Posting Time
</p>
""", unsafe_allow_html=True)

# =================================================
# KPI CARDS
# =================================================
c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown(f"""
<div class="metric-card blue glow">
<h3>Total Engagement</h3>
<h2>{int(filtered_df["engagement"].sum())}</h2>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="metric-card green">
<h3>Avg Engagement Rate</h3>
<h2>{round(filtered_df["engagement_rate"].mean(),2)}%</h2>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="metric-card orange">
<h3>Ad Spend</h3>
<h2>₹ {int(filtered_df["ad_spend"].sum())}</h2>
</div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class="metric-card red glow">
<h3>Revenue Generated</h3>
<h2>₹ {int(filtered_df["revenue_generated"].sum())}</h2>
</div>
""", unsafe_allow_html=True)

c5.markdown(f"""
<div class="metric-card purple">
<h3>Avg ROI</h3>
<h2>{round(filtered_df["roi"].mean(),2)}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="progress-bar"></div>', unsafe_allow_html=True)

# =================================================
# TABS
# =================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📱 Engagement", "🖼️ Content", "💰 Campaign ROI", "⏰ Best Time"]
)

# ---------------- TAB 1 ----------------
with tab1:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    platform_eng = filtered_df.groupby("platform")["engagement_rate"].mean().reset_index()
    st.bar_chart(platform_eng, x="platform", y="engagement_rate")
    best_platform = platform_eng.loc[platform_eng["engagement_rate"].idxmax(),"platform"]
    st.success(f"🏆 Best Platform: **{best_platform}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TAB 2 ----------------
with tab2:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    content_perf = filtered_df.groupby("content_type")[["likes","comments","shares","engagement"]].mean().reset_index()
    st.dataframe(content_perf)
    st.bar_chart(content_perf, x="content_type", y="engagement")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TAB 3 ----------------
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    campaign_df = filtered_df[filtered_df["campaign_name"].notna()]
    campaign_summary = campaign_df.groupby("campaign_name")[["ad_spend","revenue_generated","roi"]].mean().reset_index()
    st.dataframe(campaign_summary)
    st.bar_chart(campaign_summary, x="campaign_name", y="revenue_generated")
    st.bar_chart(campaign_summary, x="campaign_name", y="roi")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TAB 4 ----------------
with tab4:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    hourly = filtered_df.groupby("post_hour")["engagement"].mean().reset_index()
    st.line_chart(hourly, x="post_hour", y="engagement")
    best_hour = hourly.loc[hourly["engagement"].idxmax(),"post_hour"]
    st.success(f"🔥 Best Posting Time: **{best_hour}:00 hrs**")
    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# FOOTER
# =================================================
st.markdown("""
<hr>
<p style="text-align:center;color:#bbbbbb;">
Project 8 • Social Media Engagement Analytics • Built with ❤️ & Streamlit
</p>
""", unsafe_allow_html=True)
