# Research Project Plan: Skills-Based Hiring Sentiment Analysis

## Project Overview

**Title:** Reddit Discourse Analysis — Public Sentiment on Skills-Based Hiring Reform
**Principal Investigator:** Xavier Rivera
**Organization:** Opportunity@Work (contract engagement)
**Start Date:** January 15, 2025
**End Date:** April 30, 2025
**Status:** Complete

---

## 1. Objectives

1. **Map public sentiment** around skills-based hiring across federal employment and career subreddits
2. **Identify key themes** — what concerns, hopes, and misconceptions dominate the conversation
3. **Track sentiment over time** to detect shifts correlated with policy announcements or RIF events
4. **Produce an interactive dashboard** and summary report for leadership to guide communications strategy

---

## 2. Scope

| Dimension | Detail |
|---|---|
| **Data source** | Reddit (via PRAW API and Pushshift) |
| **Subreddits** | r/FedEmployees, r/feddiscussion, r/govfire, r/deptHHS, r/humanresources, r/recruiting, r/jobs, r/careerguidance |
| **Time window** | Jan 2022 – Jun 2025 |
| **Content types** | Submissions (posts) and top-level comments |
| **Analysis methods** | NLP sentiment scoring, keyword frequency analysis, engagement metrics |
| **Deliverables** | Cleaned dataset, Streamlit dashboard, summary report, research documentation |

---

## 3. Workstreams

### WS1: Data Collection (Weeks 1–3)
- Configure Reddit API credentials and Pushshift access
- Develop and test collection scripts for target subreddits
- Run initial data pulls; validate completeness
- Store raw data with provenance metadata

### WS2: Data Cleaning & Enrichment (Weeks 3–5)
- Deduplicate records across collection methods
- Parse timestamps, handle missing values
- Compute derived fields: sentiment score, word count, engagement tier
- Document all cleaning decisions in code and data dictionary

### WS3: Analysis & Visualization (Weeks 5–8)
- Exploratory data analysis — volume trends, top subreddits, engagement patterns
- Sentiment time-series by subreddit and content type
- Keyword frequency tracking for skills-based hiring terminology
- Build interactive Streamlit dashboard with filters

### WS4: Reporting & Handoff (Weeks 8–10)
- Draft executive summary with top findings
- Package cleaned dataset with documentation
- Deploy dashboard for stakeholder review
- Conduct walkthrough with leadership team

---

## 4. Timeline

| Week | Dates | Milestone | Workstream |
|------|-------|-----------|------------|
| 1 | Jan 15–19 | API access configured, scripts tested | WS1 |
| 2 | Jan 22–26 | First data pull complete (federal subs) | WS1 |
| 3 | Jan 29–Feb 2 | Full data pull complete; cleaning begins | WS1 → WS2 |
| 4 | Feb 5–9 | Deduplication and enrichment complete | WS2 |
| 5 | Feb 12–16 | Data dictionary finalized; EDA begins | WS2 → WS3 |
| 6 | Feb 19–23 | Core visualizations built | WS3 |
| 7 | Feb 26–Mar 2 | Dashboard v1 deployed internally | WS3 |
| 8 | Mar 5–9 | Dashboard feedback incorporated | WS3 → WS4 |
| 9 | Mar 12–16 | Executive summary drafted | WS4 |
| 10 | Mar 19–23 | Final deliverables packaged and handed off | WS4 |

---

## 5. Team Roles

| Role | Person | Responsibilities |
|------|--------|-----------------|
| **Principal Investigator** | Xavier Rivera | Research design, analysis oversight, final report |
| **Data Analyst** | Xavier Rivera | Script development, data cleaning, dashboard build |
| **Project Coordinator** | Xavier Rivera | Timeline tracking, stakeholder communication |
| **Stakeholder Lead** | OAW Program Director | Requirements input, review and approval |

---

## 6. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | Reddit API rate limiting delays data collection | Medium | Medium | Implement exponential backoff; stagger pulls across days |
| R2 | Pushshift API downtime or deprecation | High | High | Maintain PRAW as fallback; cache all raw pulls immediately |
| R3 | Low post volume in niche subreddits | Medium | Low | Expand keyword list; include adjacent subreddits |
| R4 | Sentiment model misclassifies sarcasm/irony | Medium | Medium | Use manual spot-check sample (n=50) to calibrate; report confidence intervals |
| R5 | Scope creep from stakeholder requests | Low | High | Document scope in this plan; route change requests through PI |
| R6 | PII exposure in Reddit data | Low | High | Strip author usernames before sharing; no re-identification attempts |

---

## 7. Key Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| Jan 15 | Use both PRAW and Pushshift for collection | PRAW gives real-time data; Pushshift gives historical depth | Xavier Rivera |
| Jan 20 | Set minimum score threshold at 5 upvotes | Filters low-quality/spam content while preserving signal | Xavier Rivera |
| Feb 5 | Add `engagement_tier` derived column | Enables filtering by post impact level in dashboard | Xavier Rivera |
| Feb 20 | Deploy on Streamlit Community Cloud | Free, purpose-built for Streamlit, auto-deploys from GitHub | Xavier Rivera |

---

## 8. Deliverables Checklist

- [x] Raw dataset with provenance metadata
- [x] Cleaned dataset with data dictionary
- [x] Data collection scripts (PRAW + Pushshift)
- [x] Documented cleaning pipeline
- [x] Interactive Streamlit dashboard
- [x] Executive summary and key findings
- [x] Research project plan (this document)
- [x] Task tracker
