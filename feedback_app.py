import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pulse · Feedback System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Root Variables ─── */
:root {
    --bg-primary:   #0d0f14;
    --bg-secondary: #151820;
    --bg-card:      #1c2030;
    --accent-1:     #f5c842;
    --accent-2:     #ff6b6b;
    --accent-3:     #4ecdc4;
    --text-primary: #e8eaf0;
    --text-muted:   #6b7280;
    --border:       #252a3a;
}

/* ─── Base Reset ─── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: var(--bg-primary);
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(245,200,66,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(78,205,196,0.05) 0%, transparent 50%);
}

/* ─── Hide Streamlit Branding ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    transition: color 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--accent-1) !important;
}

/* ─── Headings ─── */
h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem !important;
    letter-spacing: -0.02em;
    color: var(--text-primary) !important;
    line-height: 1.1 !important;
}
h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem !important;
    color: var(--text-primary) !important;
}
h3 {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem !important;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
}

/* ─── Metric Cards ─── */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: var(--accent-1);
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.2rem !important;
    color: var(--text-primary) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted) !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ─── Buttons ─── */
.stButton > button {
    background: var(--accent-1);
    color: #0d0f14;
    border: none;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.55rem 1.6rem;
    transition: all 0.2s;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    background: #ffd44f;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(245,200,66,0.3);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ─── Inputs ─── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent-1) !important;
    box-shadow: 0 0 0 3px rgba(245,200,66,0.12) !important;
}

/* ─── Slider ─── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background-color: var(--accent-1) !important;
    border-color: var(--accent-1) !important;
}
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* ─── Dataframe / Table ─── */
.stDataFrame {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* ─── Divider ─── */
hr {
    border-color: var(--border) !important;
}

/* ─── Radio Buttons ─── */
.stRadio [data-testid="stWidgetLabel"] {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
}

/* ─── Star Rating Custom ─── */
.star-row {
    display: flex;
    gap: 6px;
    margin: 0.4rem 0 1rem;
}
.star-btn {
    font-size: 1.8rem;
    cursor: pointer;
    transition: transform 0.15s;
    user-select: none;
}
.star-btn:hover { transform: scale(1.25); }

/* ─── Tag Pill ─── */
.tag-pill {
    display: inline-block;
    background: rgba(245,200,66,0.12);
    border: 1px solid rgba(245,200,66,0.3);
    color: var(--accent-1);
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 20px;
    margin: 2px;
}
.tag-pill-neg {
    background: rgba(255,107,107,0.12);
    border: 1px solid rgba(255,107,107,0.3);
    color: var(--accent-2);
}
.tag-pill-neu {
    background: rgba(78,205,196,0.12);
    border: 1px solid rgba(78,205,196,0.3);
    color: var(--accent-3);
}

/* ─── Success / Info Boxes ─── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ─── Expander ─── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* ─── Progress Bar ─── */
.stProgress > div > div {
    background: var(--accent-1) !important;
    border-radius: 4px !important;
}

/* ─── Checkbox ─── */
.stCheckbox label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: var(--text-primary);
}

/* ─── Custom Feedback Card ─── */
.feedback-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.feedback-card:hover { border-color: rgba(245,200,66,0.4); }
.feedback-card .fc-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}
.feedback-card .fc-text {
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-primary);
}
.fc-stars { font-size: 1rem; letter-spacing: 2px; }

/* ─── Hero Banner ─── */
.hero-banner {
    background: linear-gradient(135deg, rgba(245,200,66,0.08) 0%, rgba(78,205,196,0.05) 100%);
    border: 1px solid rgba(245,200,66,0.15);
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 2rem;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-1);
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data Storage ─────────────────────────────────────────────────────────────
DATA_FILE = "feedback_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_sentiment(rating):
    if rating >= 4: return "positive"
    if rating == 3: return "neutral"
    return "negative"

def get_stars(rating):
    return "★" * rating + "☆" * (5 - rating)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.2rem 0 0.5rem;'>
        <div style='font-family:"DM Serif Display",serif; font-size:1.6rem; color:#e8eaf0;'>Pulse</div>
        <div style='font-family:"DM Mono",monospace; font-size:0.68rem; letter-spacing:0.12em;
                    text-transform:uppercase; color:#6b7280; margin-top:2px;'>Feedback System</div>
    </div>
    <hr style='border-color:#252a3a; margin: 0.8rem 0 1.4rem;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        ["Submit Feedback", "Dashboard", "Response Manager", "Settings"],
        label_visibility="visible",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    all_data = load_data()
    total = len(all_data)
    avg = round(sum(d["rating"] for d in all_data) / total, 1) if total else 0
    pending = sum(1 for d in all_data if not d.get("responded", False))

    st.markdown(f"""
    <div style='background:#1c2030; border:1px solid #252a3a; border-radius:10px; padding:1rem 1.2rem;'>
        <div style='font-family:"DM Mono",monospace; font-size:0.68rem; text-transform:uppercase;
                    letter-spacing:0.1em; color:#6b7280; margin-bottom:0.6rem;'>Quick Stats</div>
        <div style='display:flex; justify-content:space-between; margin-bottom:0.3rem;'>
            <span style='font-size:0.85rem; color:#9ca3af;'>Total entries</span>
            <span style='font-family:"DM Mono",monospace; color:#f5c842;'>{total}</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:0.3rem;'>
            <span style='font-size:0.85rem; color:#9ca3af;'>Avg rating</span>
            <span style='font-family:"DM Mono",monospace; color:#f5c842;'>{avg} / 5</span>
        </div>
        <div style='display:flex; justify-content:space-between;'>
            <span style='font-size:0.85rem; color:#9ca3af;'>Pending replies</span>
            <span style='font-family:"DM Mono",monospace; color:#ff6b6b;'>{pending}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page: Submit Feedback ─────────────────────────────────────────────────────
if page == "Submit Feedback":
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-label'>✦ Share Your Thoughts</div>
        <div style='font-family:"DM Serif Display",serif; font-size:2rem; line-height:1.2; color:#e8eaf0;'>
            We read every<br><em>single</em> response.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            name = st.text_input("Your name", placeholder="e.g. Jordan Smith")
            email = st.text_input("Email address", placeholder="jordan@example.com")

        with col2:
            category = st.selectbox(
                "Category",
                ["Product", "Customer Support", "Onboarding", "Performance", "Feature Request", "Other"],
            )
            source = st.selectbox(
                "How did you hear about us?",
                ["Organic", "Referral", "Social Media", "Ad", "Event"],
            )

        st.markdown("---")
        st.markdown("### Overall Rating")
        rating = st.slider("", 1, 5, 3, format="%d ★")
        star_display = get_stars(rating)
        colors = {5: "#f5c842", 4: "#a8e6cf", 3: "#4ecdc4", 2: "#ffa07a", 1: "#ff6b6b"}
        st.markdown(
            f"<div style='font-size:1.6rem; letter-spacing:4px; color:{colors[rating]};'>{star_display}</div>",
            unsafe_allow_html=True,
        )

        feedback_text = st.text_area(
            "Your feedback",
            placeholder="Tell us what you think — what worked brilliantly, what frustrated you, what you'd love to see...",
            height=130,
        )

        st.markdown("### Tags  *(optional)*")
        tag_cols = st.columns(4)
        TAGS = ["UI/UX", "Speed", "Reliability", "Support", "Value", "Docs", "Onboarding", "API"]
        selected_tags = []
        for i, tag in enumerate(TAGS):
            with tag_cols[i % 4]:
                if st.checkbox(tag, key=f"tag_{tag}"):
                    selected_tags.append(tag)

        nps = st.slider(
            "How likely are you to recommend us? (0 = not at all, 10 = definitely)",
            0, 10, 7, format="%d / 10"
        )

        submitted = st.form_submit_button("Submit Feedback →", use_container_width=True)

    if submitted:
        if not name or not feedback_text:
            st.error("Please fill in your name and feedback before submitting.")
        else:
            entry = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "timestamp": datetime.now().isoformat(),
                "name": name,
                "email": email,
                "category": category,
                "source": source,
                "rating": rating,
                "feedback": feedback_text,
                "tags": selected_tags,
                "nps": nps,
                "sentiment": get_sentiment(rating),
                "responded": False,
                "response": "",
            }
            data = load_data()
            data.append(entry)
            save_data(data)
            st.success(f"✓ Thank you, {name}! Your feedback has been recorded.")
            st.balloons()

# ── Page: Dashboard ───────────────────────────────────────────────────────────
elif page == "Dashboard":
    st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; margin-top:-0.8rem; margin-bottom:1.5rem;'>Analytics & Insights</p>",
                unsafe_allow_html=True)

    data = load_data()
    if not data:
        st.info("No feedback yet. Submit some responses first!")
        st.stop()

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    total = len(df)
    avg_rating = df["rating"].mean()
    avg_nps = df["nps"].mean() if "nps" in df.columns else 0
    pos_pct = round(len(df[df["sentiment"] == "positive"]) / total * 100)
    pending = df[~df["responded"]].shape[0]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Responses", total)
    c2.metric("Avg Rating", f"{avg_rating:.1f} / 5")
    c3.metric("Avg NPS", f"{avg_nps:.1f} / 10")
    c4.metric("Positive %", f"{pos_pct}%")
    c5.metric("Pending Replies", pending)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### Rating Distribution")
        rating_counts = df["rating"].value_counts().sort_index()
        fig_bar = go.Figure(go.Bar(
            x=[f"{'★'*i}" for i in rating_counts.index],
            y=rating_counts.values,
            marker_color=["#ff6b6b", "#ffa07a", "#4ecdc4", "#a8e6cf", "#f5c842"],
            text=rating_counts.values,
            textposition="outside",
        ))
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Mono", color="#9ca3af", size=12),
            showlegend=False,
            height=280,
            margin=dict(l=0, r=0, t=20, b=0),
            yaxis=dict(gridcolor="#252a3a", zeroline=False),
            xaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown("### Sentiment Breakdown")
        sent_counts = df["sentiment"].value_counts()
        fig_pie = go.Figure(go.Pie(
            labels=sent_counts.index.str.capitalize(),
            values=sent_counts.values,
            hole=0.6,
            marker_colors=["#f5c842", "#4ecdc4", "#ff6b6b"],
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Mono", color="#9ca3af", size=12),
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            height=280,
            margin=dict(l=0, r=0, t=20, b=0),
        )
        fig_pie.update_traces(textfont_color="#e8eaf0")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### Feedback Over Time")
    daily = df.groupby("date").size().reset_index(name="count")
    fig_line = px.area(
        daily, x="date", y="count",
        color_discrete_sequence=["#f5c842"],
    )
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono", color="#9ca3af", size=11),
        height=220,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#252a3a", zeroline=False),
        showlegend=False,
    )
    fig_line.update_traces(fillcolor="rgba(245,200,66,0.1)", line_width=2)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### Category & Source Breakdown")
    cc1, cc2 = st.columns(2)
    with cc1:
        cat_counts = df["category"].value_counts()
        fig_cat = px.bar(
            cat_counts, orientation="h",
            color_discrete_sequence=["#4ecdc4"],
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Mono", color="#9ca3af", size=11),
            height=240, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(gridcolor="#252a3a"), yaxis=dict(showgrid=False),
            showlegend=False,
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with cc2:
        src_counts = df["source"].value_counts() if "source" in df.columns else pd.Series()
        if not src_counts.empty:
            fig_src = go.Figure(go.Pie(
                labels=src_counts.index,
                values=src_counts.values,
                hole=0.5,
                marker_colors=["#f5c842","#ff6b6b","#4ecdc4","#a8e6cf","#ffa07a"],
            ))
            fig_src.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Mono", color="#9ca3af", size=11),
                height=240, margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            fig_src.update_traces(textfont_color="#e8eaf0")
            st.plotly_chart(fig_src, use_container_width=True)

    with st.expander("▾ Raw Data Table"):
        display_cols = ["timestamp", "name", "category", "rating", "nps", "sentiment", "responded"]
        st.dataframe(
            df[[c for c in display_cols if c in df.columns]].sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

# ── Page: Response Manager ────────────────────────────────────────────────────
elif page == "Response Manager":
    st.markdown("<h1>Response Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; margin-top:-0.8rem; margin-bottom:1.5rem;'>Review & reply to feedback</p>",
                unsafe_allow_html=True)

    data = load_data()
    if not data:
        st.info("No feedback yet.")
        st.stop()

    # Filters
    f1, f2, f3 = st.columns(3)
    with f1:
        filter_sent = st.selectbox("Sentiment", ["All", "Positive", "Neutral", "Negative"])
    with f2:
        filter_status = st.selectbox("Status", ["All", "Pending", "Responded"])
    with f3:
        filter_cat = st.selectbox("Category", ["All"] + list({d["category"] for d in data}))

    filtered = data[:]
    if filter_sent != "All":
        filtered = [d for d in filtered if d["sentiment"] == filter_sent.lower()]
    if filter_status == "Pending":
        filtered = [d for d in filtered if not d.get("responded")]
    elif filter_status == "Responded":
        filtered = [d for d in filtered if d.get("responded")]
    if filter_cat != "All":
        filtered = [d for d in filtered if d["category"] == filter_cat]

    filtered.sort(key=lambda x: x["timestamp"], reverse=True)
    st.markdown(f"<div style='font-family:\"DM Mono\",monospace; font-size:0.75rem; color:#6b7280; margin-bottom:1rem; letter-spacing:0.08em;'>SHOWING {len(filtered)} RESULT(S)</div>", unsafe_allow_html=True)

    for entry in filtered:
        sent = entry.get("sentiment", "neutral")
        pill_cls = "tag-pill" if sent == "positive" else ("tag-pill-neg" if sent == "negative" else "tag-pill-neu")
        stars_html = f"<span class='fc-stars' style='color:{'#f5c842' if sent=='positive' else ('#ff6b6b' if sent=='negative' else '#4ecdc4')};'>{get_stars(entry['rating'])}</span>"
        tags_html = " ".join(f"<span class='tag-pill'>{t}</span>" for t in entry.get("tags", []))
        responded_badge = (
            "<span style='background:rgba(168,230,207,0.15);border:1px solid rgba(168,230,207,0.3);"
            "color:#a8e6cf;font-family:DM Mono,monospace;font-size:0.65rem;padding:2px 8px;border-radius:20px;"
            "letter-spacing:0.06em;text-transform:uppercase;'>✓ Replied</span>"
            if entry.get("responded") else
            "<span style='background:rgba(255,107,107,0.1);border:1px solid rgba(255,107,107,0.3);"
            "color:#ff6b6b;font-family:DM Mono,monospace;font-size:0.65rem;padding:2px 8px;border-radius:20px;"
            "letter-spacing:0.06em;text-transform:uppercase;'>Pending</span>"
        )

        st.markdown(f"""
        <div class='feedback-card'>
            <div class='fc-meta'>
                {stars_html} &nbsp;·&nbsp; {entry['name']} &nbsp;·&nbsp;
                {entry['category']} &nbsp;·&nbsp;
                {entry['timestamp'][:10]} &nbsp;·&nbsp; NPS: {entry.get('nps','—')}
                &nbsp;&nbsp;{responded_badge}
            </div>
            <div class='fc-text'>"{entry['feedback']}"</div>
            {'<div style="margin-top:0.5rem;">' + tags_html + '</div>' if tags_html else ''}
        </div>
        """, unsafe_allow_html=True)

        if not entry.get("responded"):
            with st.expander(f"↳ Reply to {entry['name']}"):
                resp_text = st.text_area(
                    "Your response", key=f"resp_{entry['id']}",
                    placeholder="Write a thoughtful reply...",
                    height=100,
                )
                if st.button("Send Reply", key=f"btn_{entry['id']}"):
                    if resp_text:
                        for i, d in enumerate(data):
                            if d["id"] == entry["id"]:
                                data[i]["responded"] = True
                                data[i]["response"] = resp_text
                                data[i]["response_time"] = datetime.now().isoformat()
                        save_data(data)
                        st.success("Reply saved!")
                        st.rerun()
        else:
            with st.expander("↳ View your reply"):
                st.markdown(
                    f"<div style='background:#1c2030;border:1px solid #252a3a;border-radius:8px;"
                    f"padding:0.8rem 1rem;font-size:0.9rem;color:#9ca3af;'>{entry.get('response','—')}</div>",
                    unsafe_allow_html=True,
                )

# ── Page: Settings ────────────────────────────────────────────────────────────
elif page == "Settings":
    st.markdown("<h1>Settings</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; margin-top:-0.8rem; margin-bottom:1.5rem;'>Configure your feedback system</p>",
                unsafe_allow_html=True)

    data = load_data()

    with st.expander("▾ Export Data"):
        if data:
            df_export = pd.DataFrame(data)
            csv = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇ Download CSV",
                csv,
                "feedback_export.csv",
                "text/csv",
                use_container_width=False,
            )
            json_str = json.dumps(data, indent=2)
            st.download_button(
                "⬇ Download JSON",
                json_str,
                "feedback_export.json",
                "application/json",
            )
        else:
            st.info("No data to export yet.")

    with st.expander("▾ Danger Zone"):
        st.warning("⚠ This will permanently delete all feedback data.")
        confirm = st.checkbox("I understand this action is irreversible")
        if confirm:
            if st.button("🗑 Clear All Feedback", type="primary"):
                save_data([])
                st.success("All feedback has been cleared.")
                st.rerun()

    with st.expander("▾ About"):
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.8rem; color:#9ca3af; line-height:1.8;'>
        <strong style='color:#f5c842;'>Pulse</strong> — Interactive Feedback System<br>
        Built with Streamlit · Plotly · Python<br><br>
        <strong>Features:</strong><br>
        ✦ Multi-field feedback form with star ratings & NPS<br>
        ✦ Real-time analytics dashboard<br>
        ✦ Sentiment auto-detection<br>
        ✦ Response manager with reply threading<br>
        ✦ CSV / JSON export<br>
        ✦ Persistent local storage<br>
        </div>
        """, unsafe_allow_html=True)
