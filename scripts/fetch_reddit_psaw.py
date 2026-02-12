#!/usr/bin/env python3
"""
Fetch historical Reddit submissions via Pushshift API (PSAW wrapper).

Targets career and HR subreddits for broader skills-based hiring discourse.
"""
import datetime
import pandas as pd
from psaw import PushshiftAPI

# 1) Initialize PSAW with custom base URL
api = PushshiftAPI(
    network_request_args={"headers": {"User-Agent": "Mozilla/5.0"}}
)
api.base_url = "https://api.pushshift.io/reddit"

# 2) Define search scope
subreddits = ["humanresources", "recruiting", "jobs", "careerguidance"]
keywords = ["hiring", "skills"]
after = int(datetime.datetime(2022, 1, 1).timestamp())
before = int(datetime.datetime(2025, 7, 24).timestamp())

# 3) Fetch submissions
gen = api.search_submissions(
    subreddit=subreddits,
    q=" OR ".join(keywords),
    after=after,
    before=before,
    filter=["id", "title", "selftext", "created_utc", "score", "subreddit"],
    limit=500,
)

# 4) Collect into DataFrame
posts = []
for post in gen:
    posts.append({
        "thread_id":   post.id,
        "title":       post.title,
        "body":        post.selftext,
        "created_utc": datetime.datetime.fromtimestamp(post.created_utc),
        "score":       post.score,
        "subreddit":   post.subreddit,
    })

df = pd.DataFrame(posts)

# 5) Save
df.to_csv("reddit_skills_data.csv", index=False)
print(f"Saved {len(df)} posts to reddit_skills_data.csv")
