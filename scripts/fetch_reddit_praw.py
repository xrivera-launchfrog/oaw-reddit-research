#!/usr/bin/env python3
"""
Fetch Reddit posts and comments related to skills-based hiring using PRAW.

Targets federal employment subreddits to capture discourse around
hiring reform, RIFs, and skills-based credential evaluation.
"""
import praw
import pandas as pd
import datetime
import time
import os

# ── 1) Configure Reddit API credentials via environment variables ────────────
reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="skills_hiring_research/0.1"
)

# ── 2) Define search scope ──────────────────────────────────────────────────
subreddits = ["deptHHS", "FedEmployees", "feddiscussion", "govfire"]
keywords = ["hiring", "skills", "RIF", "applied", "hired"]

after = int(datetime.datetime(2024, 1, 1).timestamp())
before = int(datetime.datetime(2025, 6, 30).timestamp())
limit = 100          # posts per keyword per subreddit
min_score = 5        # minimum upvotes to include
sleep_sec = 1        # pause between comment fetches

# ── 3) Collect posts and comments ────────────────────────────────────────────
records = []
for sub in subreddits:
    sr = reddit.subreddit(sub)
    for kw in keywords:
        for submission in sr.search(kw, limit=limit, sort="relevance",
                                    time_filter="all"):
            if after <= submission.created_utc <= before and submission.score >= min_score:
                records.append({
                    "type":        "post",
                    "thread_id":   submission.id,
                    "id":          submission.id,
                    "title":       submission.title,
                    "body":        submission.selftext,
                    "created_utc": datetime.datetime.fromtimestamp(submission.created_utc),
                    "score":       submission.score,
                    "subreddit":   submission.subreddit.display_name,
                    "author":      str(submission.author),
                })
                submission.comments.replace_more(limit=0)
                for c in submission.comments.list():
                    if c.score >= min_score:
                        records.append({
                            "type":        "comment",
                            "thread_id":   submission.id,
                            "id":          c.id,
                            "title":       "",
                            "body":        c.body,
                            "created_utc": datetime.datetime.fromtimestamp(c.created_utc),
                            "score":       c.score,
                            "subreddit":   submission.subreddit.display_name,
                            "author":      str(c.author),
                        })
                time.sleep(sleep_sec)

# ── 4) Save combined data ────────────────────────────────────────────────────
if records:
    df_all = pd.DataFrame(records)
    outfile = "reddit_skills_combined.csv"
    df_all.to_csv(outfile, index=False)
    print(f"Saved {len(df_all)} records to {outfile}")
else:
    print("No records collected.")
