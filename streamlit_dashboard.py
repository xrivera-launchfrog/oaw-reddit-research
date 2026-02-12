import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Skills-Based Hiring Sentiment Dashboard",
    layout="wide",
)

# ── Load Data ────────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parent / "data" / "cleaned" / "reddit_skills_cleaned.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["created_utc"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = pd.to_datetime(df["month"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Data file not found at {DATA_PATH}. Run `python scripts/clean_data.py` first.")
    st.stop()

# ── Sidebar Filters ──────────────────────────────────────────────────────────
st.sidebar.header("Filters")

# Date range
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Subreddit filter
all_subs = sorted(df["subreddit"].unique())
selected_subs = st.sidebar.multiselect(
    "Subreddits",
    options=all_subs,
    default=all_subs,
)

# Content type filter
content_type = st.sidebar.radio("Content type", ["All", "Posts only", "Comments only"])

# Apply filters
mask = (
    (df["date"].dt.date >= date_range[0])
    & (df["date"].dt.date <= date_range[1])
    & (df["subreddit"].isin(selected_subs))
)
if content_type == "Posts only":
    mask = mask & (df["type"] == "post")
elif content_type == "Comments only":
    mask = mask & (df["type"] == "comment")
filtered = df[mask].copy()

# ── Title ────────────────────────────────────────────────────────────────────
st.title("Skills-Based Hiring Sentiment Dashboard")
st.caption("Reddit discourse analysis for Opportunity@Work — Xavier Rivera")

if filtered.empty:
    st.warning("No data matches the current filters. Adjust the sidebar filters.")
    st.stop()

# ── Section 1: Executive Summary ─────────────────────────────────────────────
st.header("1. Executive Summary")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Records", f"{len(filtered):,}")
with col2:
    total_posts = (filtered["type"] == "post").sum()
    st.metric("Posts", f"{total_posts:,}")
with col3:
    total_comments = (filtered["type"] == "comment").sum()
    st.metric("Comments", f"{total_comments:,}")
with col4:
    avg_sentiment = filtered["sentiment_score"].mean()
    st.metric("Avg Sentiment", f"{avg_sentiment:+.3f}")
with col5:
    unique_threads = filtered["thread_id"].nunique()
    st.metric("Unique Threads", f"{unique_threads:,}")

# Sentiment breakdown bar
sent_counts = filtered["sentiment_label"].value_counts()
pos_pct = sent_counts.get("positive", 0) / len(filtered) * 100
neu_pct = sent_counts.get("neutral", 0) / len(filtered) * 100
neg_pct = sent_counts.get("negative", 0) / len(filtered) * 100

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Positive", f"{pos_pct:.1f}%")
with col_b:
    st.metric("Neutral", f"{neu_pct:.1f}%")
with col_c:
    st.metric("Negative", f"{neg_pct:.1f}%")

# ── Section 2: Thread vs. Post Analysis ──────────────────────────────────────
st.header("2. Post & Comment Volume Over Time")

monthly = (
    filtered.groupby(["month", "type"])
    .size()
    .reset_index(name="count")
)

volume_chart = (
    alt.Chart(monthly)
    .mark_bar(opacity=0.8)
    .encode(
        x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
        y=alt.Y("count:Q", title="Count"),
        color=alt.Color("type:N", title="Type", scale=alt.Scale(
            domain=["post", "comment"],
            range=["#4C78A8", "#F58518"],
        )),
        tooltip=["month:T", "type:N", "count:Q"],
    )
    .properties(height=350)
    .interactive()
)
st.altair_chart(volume_chart, use_container_width=True)

# Engagement distribution
st.subheader("Engagement Distribution by Content Type")
engagement_data = filtered[["type", "score"]].copy()
engagement_hist = (
    alt.Chart(engagement_data)
    .mark_bar(opacity=0.7)
    .encode(
        x=alt.X("score:Q", bin=alt.Bin(maxbins=30), title="Score"),
        y=alt.Y("count():Q", title="Count"),
        color=alt.Color("type:N", title="Type", scale=alt.Scale(
            domain=["post", "comment"],
            range=["#4C78A8", "#F58518"],
        )),
        tooltip=["type:N", "count():Q"],
    )
    .properties(height=300)
    .interactive()
)
st.altair_chart(engagement_hist, use_container_width=True)

# ── Section 3: Skills-Based Hiring Keyword Analysis ──────────────────────────
st.header("3. Skills-Based Hiring Keyword Trends")

keywords = {
    "skills-based": r"(?i)skills?.based",
    "STARs": r"(?i)\bstars?\b",
    "degree requirement": r"(?i)degree.?require",
    "hiring reform": r"(?i)hiring.?reform",
    "RIF": r"(?i)\brif\b",
    "competency": r"(?i)competen",
}

keyword_rows = []
for label, pattern in keywords.items():
    monthly_kw = (
        filtered[filtered["body"].str.contains(pattern, na=False)]
        .groupby("month")
        .size()
        .reset_index(name="mentions")
    )
    monthly_kw["keyword"] = label
    keyword_rows.append(monthly_kw)

if keyword_rows:
    kw_df = pd.concat(keyword_rows, ignore_index=True)
    kw_chart = (
        alt.Chart(kw_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
            y=alt.Y("mentions:Q", title="Mentions"),
            color=alt.Color("keyword:N", title="Keyword"),
            tooltip=["month:T", "keyword:N", "mentions:Q"],
        )
        .properties(height=350)
        .interactive()
    )
    st.altair_chart(kw_chart, use_container_width=True)
else:
    st.info("No keyword matches found in the filtered data.")

# ── Section 4: Sentiment Trends Over Time ────────────────────────────────────
st.header("4. Sentiment Trends by Subreddit")

monthly_sent = (
    filtered.groupby(["month", "subreddit"])["sentiment_score"]
    .mean()
    .reset_index()
)

sentiment_chart = (
    alt.Chart(monthly_sent)
    .mark_line(point=True, strokeWidth=2)
    .encode(
        x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
        y=alt.Y("sentiment_score:Q", title="Avg Sentiment Score"),
        color=alt.Color("subreddit:N", title="Subreddit"),
        tooltip=["month:T", "subreddit:N", alt.Tooltip("sentiment_score:Q", format=".3f")],
    )
    .properties(height=400)
    .interactive()
)
st.altair_chart(sentiment_chart, use_container_width=True)

# ── Section 5: Subreddit Comparison ──────────────────────────────────────────
st.header("5. Subreddit Comparison")

sub_stats = (
    filtered.groupby("subreddit")
    .agg(
        posts=("type", lambda x: (x == "post").sum()),
        comments=("type", lambda x: (x == "comment").sum()),
        avg_score=("score", "mean"),
        avg_sentiment=("sentiment_score", "mean"),
    )
    .reset_index()
)

# Volume comparison
sub_volume = sub_stats.melt(
    id_vars="subreddit",
    value_vars=["posts", "comments"],
    var_name="type",
    value_name="count",
)

sub_chart = (
    alt.Chart(sub_volume)
    .mark_bar(opacity=0.85)
    .encode(
        x=alt.X("subreddit:N", title="Subreddit", sort="-y"),
        y=alt.Y("count:Q", title="Count"),
        color=alt.Color("type:N", title="Type", scale=alt.Scale(
            domain=["posts", "comments"],
            range=["#4C78A8", "#F58518"],
        )),
        xOffset="type:N",
        tooltip=["subreddit:N", "type:N", "count:Q"],
    )
    .properties(height=350)
    .interactive()
)
st.altair_chart(sub_chart, use_container_width=True)

# Sentiment by subreddit
st.subheader("Average Sentiment by Subreddit")
sent_bar = (
    alt.Chart(sub_stats)
    .mark_bar()
    .encode(
        x=alt.X("subreddit:N", title="Subreddit", sort="-y"),
        y=alt.Y("avg_sentiment:Q", title="Avg Sentiment Score"),
        color=alt.condition(
            alt.datum.avg_sentiment > 0,
            alt.value("#4C78A8"),
            alt.value("#E45756"),
        ),
        tooltip=["subreddit:N", alt.Tooltip("avg_sentiment:Q", format=".3f")],
    )
    .properties(height=300)
)
st.altair_chart(sent_bar, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Built by Xavier Rivera | Data collected via Reddit API (PRAW) and Pushshift | "
    "Sentiment analysis via TextBlob | Dashboard powered by Streamlit"
)
