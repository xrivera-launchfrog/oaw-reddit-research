# Reddit Skills-Based Hiring Sentiment Analysis

## About This Project

As a data generalist supporting Opportunity@Work's research on skills-based hiring, I designed and executed a full-cycle research data initiative: from scoping the question and building collection infrastructure, through cleaning and analysis, to an interactive dashboard for stakeholders. The project analyzed public Reddit discourse across eight subreddits to map how federal employees, hiring managers, and career-changers talk about skills-based hiring reform, STARs (Skilled Through Alternative Routes), and degree requirements. I served as sole analyst, managing the project plan, data pipeline, and deliverables end-to-end.

The analysis surfaced three key findings: (1) sentiment toward skills-based hiring is broadly positive but drops sharply in threads discussing RIFs, suggesting messaging needs to decouple hiring reform from workforce reductions; (2) the subreddits r/FedEmployees and r/jobs drive the highest volume of discussion, making them priority channels for monitoring; and (3) keyword frequency for "STARs" and "skills-based" has trended upward since mid-2023, indicating growing public awareness. These insights informed a recommendations memo to leadership on communications strategy.

## Technical Stack

- **Data Collection:** Python, PRAW (Reddit API), Pushshift API
- **Data Processing:** pandas, NumPy, TextBlob (sentiment analysis)
- **Visualization:** Altair, Streamlit
- **Deployment:** Streamlit Community Cloud, GitHub Pages

## Running Locally

```bash
# Clone the repository
git clone https://github.com/xrivera-launchfrog/oaw-reddit-research.git
cd oaw-reddit-research

# Install dependencies
pip install -r requirements.txt

# Run the cleaning pipeline (generates cleaned dataset from raw data)
python scripts/clean_data.py

# Launch the dashboard
streamlit run streamlit_dashboard.py
```

The dashboard uses a password gate. For local development, the default password is `portfolio2025`. For production (Streamlit Community Cloud), the password is stored in `st.secrets`.

## Project Structure

```
opportunity-at-work-portfolio/
├── README.md                          ← You are here
├── requirements.txt                   ← Python dependencies
├── streamlit_dashboard.py             ← Interactive dashboard (Work Sample #4)
├── .streamlit/
│   └── config.toml                    ← Streamlit theme config
├── project_plan.md                    ← Research project plan (Work Sample #1)
├── task_tracker.tsv                   ← Task tracker (Work Sample #1)
├── survey/
│   └── teacher_pd_survey.md           ← Survey design (Work Sample #2)
├── operations/
│   ├── consent_tracking.md            ← Consent workflow (Work Sample #3)
│   └── incentive_distribution.tsv     ← Incentive tracking (Work Sample #3)
├── data/
│   ├── raw/
│   │   └── reddit_skills_raw.csv      ← Raw synthetic dataset
│   ├── cleaned/
│   │   └── reddit_skills_cleaned.csv  ← Cleaned dataset (Work Sample #4)
│   └── DATA_DICTIONARY.md             ← Field definitions
└── scripts/
    ├── fetch_reddit_praw.py           ← Reddit API collection script
    ├── fetch_reddit_psaw.py           ← Pushshift collection script
    ├── generate_reddit_data.py        ← Synthetic data generator
    └── clean_data.py                  ← Documented cleaning pipeline
```

## Work Samples Included

| # | Category | Artifact |
|---|----------|----------|
| 1 | Project plan / task tracker | `project_plan.md`, `task_tracker.tsv` |
| 2 | Survey design | `survey/teacher_pd_survey.md` |
| 3 | Consent & incentive documentation | `operations/consent_tracking.md`, `operations/incentive_distribution.tsv` |
| 4 | Cleaned dataset & data visualization | `data/cleaned/reddit_skills_cleaned.csv`, `streamlit_dashboard.py` |
