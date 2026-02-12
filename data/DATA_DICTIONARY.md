# Data Dictionary

## Dataset: `reddit_skills_cleaned.csv`

**Source:** Reddit posts and comments collected via PRAW (Reddit API) and Pushshift API
**Collection Period:** January 2022 – June 2025
**Record Count:** ~485 rows (after cleaning)
**Unit of Observation:** One Reddit post or comment

---

## Field Definitions

| # | Field Name | Data Type | Description | Source | Notes |
|---|-----------|-----------|-------------|--------|-------|
| 1 | `type` | string | Content type — `"post"` (submission) or `"comment"` (top-level reply) | Raw | Used to segment analysis by content level |
| 2 | `thread_id` | string | Reddit submission ID; groups posts with their comments into threads | Raw | Same as `id` for posts; parent submission ID for comments |
| 3 | `id` | string | Unique Reddit content ID | Raw | Post or comment ID; globally unique within Reddit |
| 4 | `title` | string | Submission title | Raw | Empty string for comments (comments have no title) |
| 5 | `body` | string | Full text content of the post or comment | Raw | `selftext` for posts, `body` for comments; null/empty rows dropped during cleaning |
| 6 | `created_utc` | datetime | Timestamp when the content was posted (UTC) | Raw → Parsed | Originally epoch integer; converted to `YYYY-MM-DD HH:MM:SS` |
| 7 | `score` | integer | Net upvotes (upvotes minus downvotes) at time of collection | Raw | Minimum threshold: 5 for PRAW-sourced data; no threshold for Pushshift |
| 8 | `subreddit` | string | Name of the subreddit where content was posted | Raw | e.g., `FedEmployees`, `jobs`, `humanresources` |
| 9 | `author` | string | Reddit username of the content author | Raw | Present in PRAW data; may be missing in Pushshift data; **stripped before public sharing** |

### Derived Fields (added during cleaning)

| # | Field Name | Data Type | Description | Derivation Logic |
|---|-----------|-----------|-------------|-----------------|
| 10 | `date` | date | Date portion of `created_utc` | `created_utc.date()` |
| 11 | `month` | string | Year-month string for aggregation | `created_utc.strftime('%Y-%m')` |
| 12 | `word_count` | integer | Number of words in `body` | `len(body.split())` |
| 13 | `sentiment_score` | float | Polarity score from TextBlob sentiment analysis | `TextBlob(body).sentiment.polarity`; range: -1.0 (most negative) to 1.0 (most positive) |
| 14 | `sentiment_label` | string | Categorical sentiment label | `positive` if score > 0.1, `negative` if score < -0.1, else `neutral` |
| 15 | `engagement_tier` | string | Engagement level based on score | `low` (score < 10), `medium` (10–24), `high` (25–99), `viral` (100+) |

---

## Data Quality Notes

- **Duplicates:** 12 duplicate records removed during cleaning (same `thread_id` + `id` combination from overlapping collection runs)
- **Missing values:** 3 rows with null `body` dropped; missing `title` for comments filled with empty string (expected behavior)
- **Date range:** Records outside Jan 2022 – Jun 2025 filtered out
- **Sentiment validation:** Manual review of 50 randomly sampled rows showed 84% agreement with TextBlob classifications
- **Author field:** Retained in raw data for deduplication; stripped from cleaned dataset shared externally

## File Locations

| File | Path | Description |
|------|------|-------------|
| Raw data | `data/raw/reddit_skills_raw.csv` | Unmodified collection output |
| Cleaned data | `data/cleaned/reddit_skills_cleaned.csv` | Analysis-ready dataset |
| Cleaning script | `scripts/clean_data.py` | Reproducible cleaning pipeline |
