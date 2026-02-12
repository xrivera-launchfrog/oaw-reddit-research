#!/usr/bin/env python3
"""
Data Cleaning Pipeline for Reddit Skills-Based Hiring Dataset

Reads the raw dataset, applies cleaning transformations, and outputs
an analysis-ready CSV with derived columns.

Usage:
    python scripts/clean_data.py

Input:  data/raw/reddit_skills_raw.csv
Output: data/cleaned/reddit_skills_cleaned.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path
from textblob import TextBlob

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "reddit_skills_raw.csv"
CLEAN_PATH = PROJECT_ROOT / "data" / "cleaned" / "reddit_skills_cleaned.csv"


def load_raw_data(path: Path) -> pd.DataFrame:
    """Load the raw CSV and do initial type parsing."""
    df = pd.read_csv(path, parse_dates=["created_utc"])
    print(f"Loaded {len(df)} rows from {path.name}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate records based on (thread_id, id) composite key.

    Duplicates can arise when overlapping collection runs (PRAW + Pushshift)
    capture the same content.
    """
    before = len(df)
    df = df.drop_duplicates(subset=["thread_id", "id"], keep="first")
    removed = before - len(df)
    print(f"Removed {removed} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values with field-appropriate strategies.

    - title: fill with empty string (comments don't have titles)
    - body: drop rows where body is null or empty (no text to analyze)
    - author: fill with 'unknown' (some Pushshift records lack author)
    """
    df["title"] = df["title"].fillna("")
    before = len(df)
    df = df.dropna(subset=["body"])
    df = df[df["body"].str.strip() != ""]
    dropped = before - len(df)
    print(f"Dropped {dropped} rows with missing/empty body text")

    df["author"] = df["author"].fillna("unknown")
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Extract date and month columns from created_utc for aggregation."""
    df["date"] = df["created_utc"].dt.date
    df["month"] = df["created_utc"].dt.strftime("%Y-%m")
    return df


def compute_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Compute sentiment polarity using TextBlob.

    TextBlob returns a polarity float in [-1.0, 1.0]:
      - Positive values = positive sentiment
      - Negative values = negative sentiment
      - Near zero = neutral

    We also create a categorical label for filtering.
    """
    df["sentiment_score"] = df["body"].apply(
        lambda text: TextBlob(str(text)).sentiment.polarity
    )

    # Categorical label with +-0.1 neutral band
    df["sentiment_label"] = df["sentiment_score"].apply(
        lambda s: "positive" if s > 0.1 else ("negative" if s < -0.1 else "neutral")
    )
    print(f"Sentiment distribution:\n{df['sentiment_label'].value_counts().to_string()}")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add word_count and engagement_tier columns.

    engagement_tier bins:
      - low: score < 10
      - medium: 10-24
      - high: 25-99
      - viral: 100+
    """
    df["word_count"] = df["body"].apply(lambda text: len(str(text).split()))

    df["engagement_tier"] = pd.cut(
        df["score"],
        bins=[-np.inf, 10, 25, 100, np.inf],
        labels=["low", "medium", "high", "viral"],
    )
    print(f"Engagement tier distribution:\n{df['engagement_tier'].value_counts().to_string()}")
    return df


def filter_date_range(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only records within the study period (Jan 2022 – Jun 2025)."""
    start = pd.Timestamp("2022-01-01")
    end = pd.Timestamp("2025-06-30")
    before = len(df)
    df = df[(df["created_utc"] >= start) & (df["created_utc"] <= end)]
    filtered = before - len(df)
    if filtered > 0:
        print(f"Filtered {filtered} rows outside study date range")
    return df


def main():
    print("=" * 60)
    print("Reddit Skills-Based Hiring — Data Cleaning Pipeline")
    print("=" * 60)

    df = load_raw_data(RAW_PATH)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = filter_date_range(df)
    df = parse_dates(df)
    df = compute_sentiment(df)
    df = add_derived_columns(df)

    # Ensure output directory exists
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    df.to_csv(CLEAN_PATH, index=False)
    print(f"\nSaved {len(df)} cleaned rows to {CLEAN_PATH.name}")
    print(f"Columns: {list(df.columns)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
