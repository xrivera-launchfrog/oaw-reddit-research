import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Skills-Based Hiring in Public Discourse",
    page_icon=None,
    layout="wide",
)

# ── Altair Theme ─────────────────────────────────────────────────────────────
PALETTE = ["#2C3E50", "#E67E22", "#7F8C8D", "#27AE60", "#8E44AD", "#C0392B"]

def research_theme():
    return {
        "config": {
            "background": "#FAFAFA",
            "title": {"fontSize": 14, "font": "system-ui, sans-serif", "anchor": "start", "color": "#2C3E50"},
            "axis": {
                "labelFontSize": 11,
                "titleFontSize": 12,
                "titleColor": "#2C3E50",
                "labelColor": "#5D6D7E",
                "gridColor": "#E5E7EB",
                "domainColor": "#BDC3C7",
                "tickColor": "#BDC3C7",
            },
            "axisX": {"grid": False},
            "axisY": {"gridDash": [2, 4]},
            "legend": {"labelFontSize": 11, "titleFontSize": 12, "labelColor": "#5D6D7E"},
            "view": {"stroke": None},
            "range": {"category": PALETTE},
        }
    }

alt.themes.register("research", research_theme)
alt.themes.enable("research")

# ── Load Data ────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_PATH = DATA_DIR / "cleaned" / "reddit_skills_cleaned.csv"
POLICY_PATH = DATA_DIR / "policy_events.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["created_utc"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = pd.to_datetime(df["month"])
    return df

@st.cache_data
def load_policy_events():
    pe = pd.read_csv(POLICY_PATH, parse_dates=["date"])
    return pe

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Data file not found at {DATA_PATH}. Run `python scripts/clean_data.py` first.")
    st.stop()

policy_events = load_policy_events()

# Key policy dates — each with a distinct color for chart rules, labels, and legend dots
POLICY_EVENTS = [
    {"date": pd.Timestamp("2022-03-15"), "label": "Maryland (Mar '22)", "color": "#2980B9", "dy": -8},
    {"date": pd.Timestamp("2022-04-18"), "label": "Colorado (Apr '22)", "color": "#E67E22", "dy": -22},
    {"date": pd.Timestamp("2023-06-01"), "label": "15 states (mid-'23)", "color": "#8E44AD", "dy": -8},
    {"date": pd.Timestamp("2024-06-05"), "label": "Connecticut (Jun '24)", "color": "#27AE60", "dy": -22},
]


def policy_rules_and_labels():
    """Create Altair layers for policy event vertical rules + staggered text labels,
    each event in its own color."""
    layers = []
    for evt in POLICY_EVENTS:
        evt_df = pd.DataFrame([{"date": evt["date"], "label": evt["label"]}])
        rule = (
            alt.Chart(evt_df)
            .mark_rule(strokeDash=[4, 4], strokeWidth=1.5, color=evt["color"])
            .encode(x="date:T")
        )
        label = (
            alt.Chart(evt_df)
            .mark_text(
                align="left", dx=5, dy=evt["dy"], fontSize=10,
                color=evt["color"], fontStyle="italic",
            )
            .encode(x="date:T", y=alt.value(0), text="label:N")
        )
        layers.append(rule)
        layers.append(label)
    result = layers[0]
    for layer in layers[1:]:
        result = result + layer
    return result


# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Reduce top padding */
    .block-container { padding-top: 2rem; }

    /* Stat callout cards */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        text-align: center;
    }
    .stat-card .stat-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #2C3E50;
        line-height: 1.1;
        margin-bottom: 0.25rem;
    }
    .stat-card .stat-label {
        font-size: 0.85rem;
        color: #7F8C8D;
        line-height: 1.3;
    }

    /* Section research question styling */
    .research-q {
        font-style: italic;
        color: #5D6D7E;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #BDC3C7;
        padding-left: 0.75rem;
    }

    /* Interpretive takeaway blocks */
    .takeaway {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-top: 0.75rem;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #34495E;
    }
    .takeaway strong { color: #2C3E50; }

    /* Mute dividers */
    hr { border-color: #E5E7EB !important; }

    /* Featured quote cards */
    .quote-card {
        background: #FFFFFF;
        border-left: 3px solid #2C3E50;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.9rem;
        line-height: 1.5;
        color: #34495E;
    }
    .quote-meta {
        font-size: 0.78rem;
        color: #95A5A6;
        margin-top: 0.5rem;
    }

    /* Policy event legend */
    .policy-legend {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        font-size: 0.85rem;
        line-height: 1.7;
        color: #444;
    }
    .policy-legend .legend-title {
        font-weight: 600;
        color: #2C3E50;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .policy-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Filters ──────────────────────────────────────────────────────────
st.sidebar.markdown("### Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

all_subs = sorted(df["subreddit"].unique())
selected_subs = st.sidebar.multiselect("Subreddits", options=all_subs, default=all_subs)

content_type = st.sidebar.radio("Content type", ["All", "Posts only", "Comments only"])

all_tiers = sorted(df["engagement_tier"].unique())
selected_tiers = st.sidebar.multiselect("Engagement tier", options=all_tiers, default=all_tiers)

# Apply filters
if len(date_range) == 2:
    d_start, d_end = date_range
else:
    d_start, d_end = min_date, max_date

mask = (
    (df["date"].dt.date >= d_start)
    & (df["date"].dt.date <= d_end)
    & (df["subreddit"].isin(selected_subs))
    & (df["engagement_tier"].isin(selected_tiers))
)
if content_type == "Posts only":
    mask = mask & (df["type"] == "post")
elif content_type == "Comments only":
    mask = mask & (df["type"] == "comment")

filtered = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing {len(filtered):,} of {len(df):,} records**")

# ── Section 1: Title & Research Context ──────────────────────────────────────
st.markdown("# Skills-Based Hiring in Public Discourse")
st.markdown(
    "*How Reddit communities discuss workforce reform, degree requirements, and the opportunity gap*"
)

st.markdown("""
In the United States, over 70 million workers are **Skilled Through Alternative Routes (STARs)** —
they have the skills employers need but lack a four-year degree. A growing body of research documents
the "paper ceiling" that excludes these workers from quality jobs despite demonstrated competency.
This dashboard explores how public discourse on Reddit reflects — and sometimes anticipates — the
policy shifts that have made skills-based hiring a bipartisan priority across 25 states.
""")

# Stat callout cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">70M+</div>
        <div class="stat-label">Workers are STARs in the US</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">25</div>
        <div class="stat-label">States committed to removing degree requirements</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">2.5pp</div>
        <div class="stat-label">Annual decline in degree requirements per year of policy exposure</div>
    </div>
    """, unsafe_allow_html=True)

st.caption("Blair, Debroy & Heck 2021; Heck, Corcoran de Castillo, Blair & Debroy 2024")

if filtered.empty:
    st.warning("No data matches the current filters. Adjust the sidebar filters.")
    st.stop()

# ── Section 2: Discourse Volume & Policy Events ─────────────────────────────
st.markdown("---")
st.markdown("## Discourse Volume & Policy Events")
st.markdown('<p class="research-q">Does online discussion of skills-based hiring track with real-world policy action?</p>', unsafe_allow_html=True)

st.markdown("""
Heck et al. (2024) found that state-level commitments to skills-based hiring produced a
measurable 2.5 percentage-point annual decline in degree-required job postings. If policy
is moving the needle on employer behavior, we should expect public discourse to reflect
that shift. The chart below overlays four key policy milestones against monthly Reddit
discussion volume.
""")

monthly = (
    filtered.groupby(["month", "type"])
    .size()
    .reset_index(name="count")
)

bars = (
    alt.Chart(monthly)
    .mark_bar(opacity=0.85)
    .encode(
        x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
        y=alt.Y("count:Q", title="Records", stack="zero"),
        color=alt.Color(
            "type:N",
            title="Type",
            scale=alt.Scale(domain=["post", "comment"], range=["#2C3E50", "#7F8C8D"]),
        ),
        tooltip=[
            alt.Tooltip("month:T", title="Month", format="%B %Y"),
            "type:N",
            "count:Q",
        ],
    )
    .properties(height=350)
)

volume_chart = (bars + policy_rules_and_labels()).interactive()
st.altair_chart(volume_chart, use_container_width=True)

# Policy events legend with context — dot colors match chart lines
st.markdown("""
<div class="policy-legend">
    <div class="legend-title">Policy Milestones</div>
    <span class="policy-dot" style="background:#2980B9"></span><strong>Maryland (Mar 2022)</strong> — First state to
    eliminate four-year degree requirements for thousands of state government positions,
    launching a wave of executive action nationwide.<br>
    <span class="policy-dot" style="background:#E67E22"></span><strong>Colorado (Apr 2022)</strong> — Governor Polis
    signed an executive order directing state agencies to adopt skills-based hiring practices
    and review existing degree requirements.<br>
    <span class="policy-dot" style="background:#8E44AD"></span><strong>15 states committed (mid-2023)</strong> — By
    mid-2023, governors from both parties had signed skills-based hiring orders or legislation,
    representing the tipping point identified in Heck et al. (2024).<br>
    <span class="policy-dot" style="background:#27AE60"></span><strong>Connecticut (Jun 2024)</strong> — Signed
    skills-first hiring into law, moving beyond executive order to durable legislation — a
    signal that reform is becoming institutionalized rather than administration-dependent.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="takeaway">
    <strong>Takeaway:</strong> Discussion volume is not uniformly distributed — it clusters
    around policy events and workforce disruptions. The Maryland executive order in March 2022
    coincides with the beginning of sustained engagement in federal employment subreddits.
    Notably, some discourse spikes <em>precede</em> formal state action, suggesting that
    public pressure and media coverage may be contributing to the policy momentum documented
    by Heck et al. The mid-2023 period — when 15 states had committed — marks an inflection
    point in both policy and discourse.
</div>
""", unsafe_allow_html=True)

# ── Section 3: Sentiment Landscape ───────────────────────────────────────────
st.markdown("---")
st.markdown("## Sentiment Landscape")
st.markdown('<p class="research-q">How does the tone of discourse vary across communities?</p>', unsafe_allow_html=True)

st.markdown("""
Blair et al. (2021) argued that the "paper ceiling" is sustained not just by formal
requirements but by cultural assumptions about degree-holders' competence. If those
assumptions are shifting in public discourse, we would expect sentiment toward skills-based
hiring to be broadly positive — but the degree of positivity may vary by community context.
""")

col_left, col_right = st.columns(2)

# Left: Average sentiment by subreddit (horizontal bar)
sub_sentiment = (
    filtered.groupby("subreddit")["sentiment_score"]
    .mean()
    .reset_index()
    .sort_values("sentiment_score")
)

with col_left:
    st.markdown("#### Average Sentiment by Subreddit")
    sent_bar = (
        alt.Chart(sub_sentiment)
        .mark_bar(cornerRadiusEnd=3)
        .encode(
            y=alt.Y("subreddit:N", title=None, sort=alt.EncodingSortField("sentiment_score", order="ascending")),
            x=alt.X("sentiment_score:Q", title="Average Sentiment"),
            color=alt.condition(
                alt.datum.sentiment_score > 0,
                alt.value("#2C3E50"),
                alt.value("#C0392B"),
            ),
            tooltip=["subreddit:N", alt.Tooltip("sentiment_score:Q", format=".3f")],
        )
        .properties(height=250)
    )
    st.altair_chart(sent_bar, use_container_width=True)

# Right: Sentiment distribution histogram for filtered data
with col_right:
    st.markdown("#### Sentiment Distribution")
    sent_hist = (
        alt.Chart(filtered)
        .mark_bar(opacity=0.8, cornerRadiusEnd=2)
        .encode(
            x=alt.X("sentiment_score:Q", bin=alt.Bin(maxbins=30), title="Sentiment Score"),
            y=alt.Y("count():Q", title="Count"),
            color=alt.value("#2C3E50"),
            tooltip=["count():Q"],
        )
        .properties(height=250)
    )
    st.altair_chart(sent_hist, use_container_width=True)

st.markdown("""
<div class="takeaway">
    <strong>Takeaway:</strong> Overall sentiment skews positive, consistent with the
    finding from Blair et al. (2021) that public awareness of STARs is growing alongside
    support for reform. However, the distribution reveals a long negative tail — a
    meaningful minority of records express frustration, skepticism, or hostility. Subreddit
    averages mask this variance: a community like r/feddiscussion may appear neutral on
    average while containing both strong advocates and vocal skeptics. The histogram on the
    right shows this bimodal tendency more clearly than the averages alone.
</div>
""", unsafe_allow_html=True)

# Sentiment over time
st.markdown("#### Sentiment Trends Over Time")
monthly_sent = (
    filtered.groupby(["month", "subreddit"])["sentiment_score"]
    .mean()
    .reset_index()
)

sentiment_time = (
    alt.Chart(monthly_sent)
    .mark_line(point=alt.OverlayMarkDef(size=30), strokeWidth=2)
    .encode(
        x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
        y=alt.Y("sentiment_score:Q", title="Avg Sentiment"),
        color=alt.Color("subreddit:N", title="Subreddit"),
        tooltip=[
            alt.Tooltip("month:T", title="Month", format="%B %Y"),
            "subreddit:N",
            alt.Tooltip("sentiment_score:Q", format=".3f"),
        ],
    )
    .properties(height=350)
    .interactive()
)
st.altair_chart(sentiment_time, use_container_width=True)

st.markdown("""
<div class="takeaway">
    <strong>Takeaway:</strong> Sentiment is not static. Periods of RIF-related anxiety
    (visible as sharp dips) depress sentiment across multiple communities simultaneously,
    suggesting that workforce reduction discourse contaminates the broader conversation
    around hiring reform. This aligns with a key concern in the Heck et al. (2024) analysis:
    that skills-based hiring risks being associated with cost-cutting rather than opportunity
    expansion if messaging is not carefully separated.
</div>
""", unsafe_allow_html=True)

# ── Section 4: Discourse Framing Analysis ────────────────────────────────────
st.markdown("---")
st.markdown("## Discourse Framing Analysis")
st.markdown('<p class="research-q">What frames dominate the conversation — and do they align with the academic findings?</p>', unsafe_allow_html=True)

st.markdown("""
Academic research on skills-based hiring operates within specific frames — equity for
STARs, the paper ceiling, and the policy mechanics of degree requirement removal. But
public discourse may organize itself differently. This section classifies each record into
five discourse frames using pattern matching, revealing how Reddit users actually talk about
these issues compared to how researchers do.
""")

FRAMES = {
    "Reform Advocacy": r"(?i)(?:skills?.based|STARs|paper.ceiling|remove.degree|hiring.reform)",
    "Skepticism & Barriers": r"(?i)(?:won'?t.change|HR.push.?back|classification.system|OPM|bureaucra)",
    "RIF & Workforce Cuts": r"(?i)(?:\bRIF\b|layoff|DOGE|reduction.in.force|\bfired\b)",
    "Practitioner Experience": r"(?i)(?:hired|my.team|my.agency|GS-\d|I'?ve.seen|in.my.experience)",
    "Career Transition": r"(?i)(?:career.chang|transition|military.to.civilian|no.degree)",
}

# Vectorized frame classification
frame_dfs = []
for frame, pattern in FRAMES.items():
    matches = filtered[filtered["body"].str.contains(pattern, na=False)]
    if not matches.empty:
        chunk = matches[["month", "sentiment_score"]].copy()
        chunk["frame"] = frame
        frame_dfs.append(chunk)

if frame_dfs:
    frame_df = pd.concat(frame_dfs, ignore_index=True)

    # Frame distribution
    frame_counts = frame_df["frame"].value_counts().reset_index()
    frame_counts.columns = ["frame", "count"]

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("#### Frame Distribution")
        frame_bar = (
            alt.Chart(frame_counts)
            .mark_bar(cornerRadiusEnd=3)
            .encode(
                y=alt.Y("frame:N", title=None, sort=alt.EncodingSortField("count", order="descending")),
                x=alt.X("count:Q", title="Records matching frame"),
                color=alt.Color("frame:N", legend=None),
                tooltip=["frame:N", "count:Q"],
            )
            .properties(height=250)
        )
        st.altair_chart(frame_bar, use_container_width=True)

    # Frame x Sentiment heatmap
    with col_f2:
        st.markdown("#### Avg Sentiment by Frame")
        frame_sent = (
            frame_df.groupby("frame")["sentiment_score"]
            .mean()
            .reset_index()
            .sort_values("sentiment_score")
        )
        heatmap = (
            alt.Chart(frame_sent)
            .mark_bar(cornerRadiusEnd=3)
            .encode(
                y=alt.Y("frame:N", title=None, sort=alt.EncodingSortField("sentiment_score", order="ascending")),
                x=alt.X("sentiment_score:Q", title="Average Sentiment"),
                color=alt.Color(
                    "sentiment_score:Q",
                    title="Sentiment",
                    scale=alt.Scale(scheme="redyellowgreen", domain=[-0.2, 0.4]),
                ),
                tooltip=["frame:N", alt.Tooltip("sentiment_score:Q", format=".3f")],
            )
            .properties(height=250)
        )
        st.altair_chart(heatmap, use_container_width=True)

    st.markdown("""
    <div class="takeaway">
        <strong>Takeaway:</strong> Reform Advocacy is the most prevalent frame, which is
        encouraging — the discourse is primarily oriented around solutions rather than
        grievances. But the sentiment gap between frames is striking. Practitioner Experience
        and Career Transition records tend to be positive: people sharing success stories
        and offering practical guidance. RIF &amp; Workforce Cuts discourse, by contrast,
        carries the most negative sentiment. This pattern matters for policy communications:
        Blair et al. (2021) emphasized that STARs succeed when given the opportunity, but
        if the loudest negative signal in public discourse comes from workforce reduction
        rather than from doubts about STARs' competence, then the messaging challenge is
        about <em>decoupling reform from austerity</em>, not about proving STARs' value.
    </div>
    """, unsafe_allow_html=True)

    # Frame trends over time
    st.markdown("#### Frame Trends Over Time")
    frame_time = (
        frame_df.groupby(["month", "frame"])
        .size()
        .reset_index(name="count")
    )
    frame_area = (
        alt.Chart(frame_time)
        .mark_area(opacity=0.7)
        .encode(
            x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
            y=alt.Y("count:Q", title="Records", stack="zero"),
            color=alt.Color("frame:N", title="Frame"),
            tooltip=[
                alt.Tooltip("month:T", title="Month", format="%B %Y"),
                "frame:N",
                "count:Q",
            ],
        )
        .properties(height=350)
        .interactive()
    )
    st.altair_chart(frame_area, use_container_width=True)

    st.caption(
        "A single record can match multiple frames. Frame classification uses pattern "
        "matching against key terms associated with each discourse category."
    )

    st.markdown("""
    <div class="takeaway">
        <strong>Takeaway:</strong> The composition of discourse shifts over time. RIF-related
        discussion tends to cluster in specific periods — often aligned with federal workforce
        reduction announcements — rather than being a constant background hum. When RIF
        discourse surges, it can temporarily dominate the conversation and crowd out Reform
        Advocacy, creating windows where the public narrative around skills-based hiring
        turns negative even though the underlying policy trend is positive.
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No discourse frames matched in the filtered data.")

# ── Section 5: Keyword Trends in Context ─────────────────────────────────────
st.markdown("---")
st.markdown("## Keyword Trends in Context")
st.markdown('<p class="research-q">Are key terms from the academic literature gaining traction in public discourse?</p>', unsafe_allow_html=True)

st.markdown("""
The research of Blair et al. (2021) introduced "STARs" and "paper ceiling" as organizing
concepts for the skills-based hiring movement. Heck et al. (2024) tracked policy adoption.
But policy impact depends partly on whether these ideas reach the people they aim to help.
This section tracks how six key terms from the academic literature appear in Reddit
discourse over time.
""")

keywords = {
    "skills-based": r"(?i)skills?.based",
    "STARs": r"(?i)\bstars?\b",
    "degree requirement": r"(?i)degree.?require",
    "paper ceiling": r"(?i)paper.ceiling",
    "competency": r"(?i)competen",
    "RIF": r"(?i)\brif\b",
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

    kw_lines = (
        alt.Chart(kw_df)
        .mark_line(point=alt.OverlayMarkDef(size=30), strokeWidth=2)
        .encode(
            x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
            y=alt.Y("mentions:Q", title="Mentions"),
            color=alt.Color("keyword:N", title="Keyword"),
            tooltip=[
                alt.Tooltip("month:T", title="Month", format="%B %Y"),
                "keyword:N",
                "mentions:Q",
            ],
        )
        .properties(height=350)
    )

    kw_chart = (kw_lines + policy_rules_and_labels()).interactive()
    st.altair_chart(kw_chart, use_container_width=True)

    st.markdown("""
    <div class="takeaway">
        <strong>Takeaway:</strong> "Skills-based" is by far the most-used term, appearing in
        over half of all records — it has successfully entered the public vocabulary.
        "STARs" and "degree requirement" show moderate adoption, typically in communities
        already engaged with federal hiring policy. But "paper ceiling" — the central
        metaphor of the Opportunity@Work research program — has <strong>zero mentions</strong>
        in this corpus. This is a significant finding: the academic framing that motivates
        the policy movement has not yet penetrated the communities it aims to serve. For
        Opportunity@Work's communications strategy, this suggests an opportunity to seed
        the "paper ceiling" concept in the same subreddits where "skills-based" already
        resonates.
    </div>
    """, unsafe_allow_html=True)

    # Keyword co-occurrence
    st.markdown("#### Keyword Co-occurrence")
    st.markdown("""
    When someone mentions one keyword, what other terms appear in the same record? High
    co-occurrence suggests concepts are linked in public understanding; low co-occurrence
    suggests they operate as separate conversations.
    """)

    co_data = []
    for primary_label, primary_pattern in keywords.items():
        primary_mask = filtered["body"].str.contains(primary_pattern, na=False)
        primary_count = primary_mask.sum()
        if primary_count == 0:
            continue
        for secondary_label, secondary_pattern in keywords.items():
            if secondary_label == primary_label:
                continue
            both = (primary_mask & filtered["body"].str.contains(secondary_pattern, na=False)).sum()
            pct = both / primary_count * 100 if primary_count > 0 else 0
            co_data.append({
                "primary": primary_label,
                "co-occurs with": secondary_label,
                "co-occurrence %": round(pct, 1),
            })

    if co_data:
        co_df = pd.DataFrame(co_data)
        co_heatmap = (
            alt.Chart(co_df)
            .mark_rect(cornerRadius=3)
            .encode(
                x=alt.X("primary:N", title="Primary Keyword"),
                y=alt.Y("co-occurs with:N", title="Co-occurring Keyword"),
                color=alt.Color(
                    "co-occurrence %:Q",
                    title="Co-occurrence %",
                    scale=alt.Scale(scheme="blues"),
                ),
                tooltip=["primary:N", "co-occurs with:N", alt.Tooltip("co-occurrence %:Q", format=".1f")],
            )
            .properties(height=250)
        )
        st.altair_chart(co_heatmap, use_container_width=True)

        st.markdown("""
        <div class="takeaway">
            <strong>Takeaway:</strong> "Skills-based" and "degree requirement" co-occur
            frequently — people discussing one tend to discuss the other, which aligns with
            the Heck et al. (2024) finding that degree requirement removal is the most
            visible policy lever. "RIF," however, shows lower co-occurrence with reform
            terminology, confirming that workforce reduction operates as a <em>separate
            discourse</em> rather than an integrated part of the hiring reform conversation.
            This is both a risk (RIF negativity bleeds into adjacent discussions) and an
            opportunity (the reform narrative can be insulated from austerity framing with
            deliberate messaging).
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No keyword matches found in the filtered data.")

# ── Section 6: Voices from the Discourse ─────────────────────────────────────
st.markdown("---")
st.markdown("## Voices from the Discourse")
st.markdown('<p class="research-q">What are people actually saying?</p>', unsafe_allow_html=True)

st.markdown("""
Quantitative analysis reveals patterns, but the individual voices behind the data give
those patterns meaning. The quotes below are the highest-upvoted records in the filtered
dataset — community-validated contributions that represent what resonates most with
these audiences. Below them, a searchable table provides access to all primary sources.
""")

# Featured quotes — top upvoted
st.markdown("#### Featured Quotes")
top_records = filtered.nlargest(5, "score")
for _, row in top_records.iterrows():
    body_text = str(row["body"])[:500]
    if len(str(row["body"])) > 500:
        body_text += "..."
    sentiment_color = "#27AE60" if row["sentiment_label"] == "positive" else (
        "#C0392B" if row["sentiment_label"] == "negative" else "#7F8C8D"
    )
    st.markdown(
        f'<div class="quote-card">{body_text}'
        f'<div class="quote-meta">r/{row["subreddit"]} · {row["date"].strftime("%b %d, %Y")} · '
        f'Score: {row["score"]} · '
        f'<span style="color:{sentiment_color}">{row["sentiment_label"]}</span></div></div>',
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="takeaway">
    <strong>Takeaway:</strong> The most-upvoted records tend to reflect lived experience —
    practitioners describing what they have seen on the ground, not abstract policy
    arguments. This aligns with Blair et al.'s emphasis on the 70 million STARs whose
    competence is demonstrated through work, not credentials. The discourse is anchored
    in personal testimony, which suggests that communications strategies built around
    individual stories may resonate more effectively than policy white papers in these
    communities.
</div>
""", unsafe_allow_html=True)

# Searchable data table
st.markdown("#### Browse All Records")
search_query = st.text_input("Search text content", placeholder="e.g. skills-based, degree, RIF...")

table_data = filtered.copy()
if search_query:
    table_data = table_data[
        table_data["body"].str.contains(search_query, case=False, na=False)
    ]

display_cols = ["date", "subreddit", "type", "sentiment_label", "score", "body"]
table_display = table_data[display_cols].copy()
table_display["date"] = table_display["date"].dt.strftime("%Y-%m-%d")
table_display = table_display.sort_values("date", ascending=False).reset_index(drop=True)

st.dataframe(
    table_display,
    column_config={
        "date": st.column_config.TextColumn("Date", width="small"),
        "subreddit": st.column_config.TextColumn("Subreddit", width="small"),
        "type": st.column_config.TextColumn("Type", width="small"),
        "sentiment_label": st.column_config.TextColumn("Sentiment", width="small"),
        "score": st.column_config.NumberColumn("Score", width="small"),
        "body": st.column_config.TextColumn("Content", width="large"),
    },
    use_container_width=True,
    height=400,
)

st.caption(f"Showing {len(table_display):,} records" + (f' matching "{search_query}"' if search_query else ""))

# ── Section 7: Methodology & Data Notes ──────────────────────────────────────
st.markdown("---")
st.markdown("## Methodology & Data Notes")

with st.expander("Data collection, processing, and limitations", expanded=False):
    st.markdown("""
**Data source:** Reddit, collected via PRAW (Python Reddit API Wrapper) and Pushshift for historical coverage.

**Collection period:** January 2022 -- June 2025

**Subreddits sampled:** r/FedEmployees, r/feddiscussion, r/govfire, r/jobs, r/recruiting,
r/humanresources, r/deptHHS, r/careerguidance

**Cleaning pipeline:**
- Deduplication (12 duplicate records removed)
- Missing value handling (3 rows with null body text dropped)
- Date parsing and month aggregation
- Sentiment scoring via TextBlob polarity (-1.0 to +1.0)
- Engagement tier binning (low / medium / high / viral)
- 15-field data dictionary maintained alongside the dataset

**Sentiment model:** TextBlob polarity scores with thresholds at +/-0.1 for positive/negative
classification. Manual validation on a random sample of n=50 records showed **84% agreement**
with human judgment. TextBlob tends to undercount sarcasm and domain-specific negativity.

**Limitations:**
- Small corpus (n=491) limits statistical power for subreddit-level comparisons
- TextBlob's lexicon-based approach has limited nuance for policy discourse
- Reddit's user base skews younger, male, and more tech-savvy than the general population
- Subreddit culture effects may drive sentiment more than topic-level factors
- Data collected under Reddit API rate limits; some threads may be missing

**Academic references:**
- Blair, P. Q., Debroy, S., & Heck, J. (2021). [Navigating with the STARs: Reimagining equitable pathways
  to mobility.](https://opportunityatwork.org/our-solutions/stars-insights/navigating-stars-report/) Opportunity@Work.
- Heck, J., Corcoran de Castillo, B., Blair, P. Q., & Debroy, S. (2024). [The Paper Ceiling: State policy
  progress on skills-based hiring.](https://opportunityatwork.org/our-solutions/stars-insights/paper-ceiling-state-policy/) Opportunity@Work.
    """)

# ── Section 8: Footer ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#95A5A6; font-size:0.85rem;">'
    "Research and analysis by Xavier Rivera | Opportunity@Work<br>"
    '<a href="https://github.com/xrivera-launchfrog/oaw-reddit-research" style="color:#7F8C8D;">GitHub</a>'
    " · "
    '<a href="https://xavierrivera.org" style="color:#7F8C8D;">Portfolio</a>'
    "</p>",
    unsafe_allow_html=True,
)
