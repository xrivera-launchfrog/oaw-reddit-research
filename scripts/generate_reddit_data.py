"""
generate_reddit_data.py
-----------------------
Creates a realistic synthetic Reddit dataset (~500 rows) about
skills-based hiring, federal employment, RIFs, and related topics.

Output: data/raw/reddit_skills_raw.csv
"""

import random
import string
import datetime
import numpy as np
import pandas as pd

# -- reproducibility -----------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# -- constants -----------------------------------------------------------------
N_ROWS = 500
POST_FRAC = 0.30
N_DUPLICATES = 15
N_EMPTY_BODY = 5

SUBREDDITS = [
    "FedEmployees", "feddiscussion", "govfire", "deptHHS",
    "humanresources", "recruiting", "jobs", "careerguidance",
]

# -- username generators -------------------------------------------------------
USERNAME_PREFIXES = [
    "federal_worker", "hr_manager_dc", "policy_wonk", "gov_analyst",
    "dc_commuter", "career_changer", "hiring_mgr", "talent_scout",
    "fed_employee", "budget_hawk", "gs13_life", "workforce_dev",
    "skills_first", "star_advocate", "public_servant", "agency_hopper",
    "telework_fan", "union_steward", "resume_guru", "usajobs_veteran",
    "data_nerd_gov", "contracting_pro", "IT_fed", "cyber_fed",
    "mil_spouse_fed", "vet_preference", "new_fed", "retired_ses",
    "hill_staffer", "think_tank_guy", "non_profit_to_gov",
    "former_teacher", "tech_to_fed", "healthcare_admin",
    "program_analyst", "management_analyst", "hr_specialist",
    "class_act_rep", "eeo_officer", "training_dev",
]


def make_username():
    base = random.choice(USERNAME_PREFIXES)
    suffix = random.choice(["", f"_{random.randint(1, 99)}", f"{random.randint(0, 9999)}"])
    return base + suffix


def reddit_id(length=6):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


# -- date helpers --------------------------------------------------------------
DATE_START = datetime.datetime(2022, 1, 1)
DATE_END = datetime.datetime(2025, 6, 30)
DATE_RANGE_SECS = int((DATE_END - DATE_START).total_seconds())

# A few dates intentionally outside the range
OUTLIER_DATES = [
    datetime.datetime(2021, 11, 15, 8, 23, 11),
    datetime.datetime(2021, 12, 3, 14, 5, 44),
    datetime.datetime(2025, 8, 12, 19, 45, 0),
    datetime.datetime(2025, 9, 1, 10, 30, 22),
]


def random_date():
    offset = random.randint(0, DATE_RANGE_SECS)
    return DATE_START + datetime.timedelta(seconds=offset)


# -- score distribution (log-normal-ish) ---------------------------------------
def random_score():
    """Most scores 5-50, some outliers up to ~500."""
    raw = np.random.lognormal(mean=2.5, sigma=0.9)
    return max(1, int(raw))


# -- realistic text pools ------------------------------------------------------

POST_TITLES = [
    "Is skills-based hiring actually happening in the federal government?",
    "OPM just released new guidance on degree requirements — thoughts?",
    "How is DOGE affecting your agency's hiring?",
    "RIF notice received — what are my options?",
    "Skills-based hiring: real reform or just a buzzword?",
    "My agency just eliminated degree requirements for GS-9 through GS-12",
    "STARs (Skilled Through Alternative Routes) — has this concept reached federal HR?",
    "Anyone else see the new executive order on federal hiring reform?",
    "Switching from private sector to federal — is USAJobs still a black hole?",
    "Degree inflation in federal job postings is getting worse",
    "Just got my first federal offer — GS-7 with no degree!",
    "How do you showcase skills on a federal resume without a degree?",
    "Our agency is piloting competency-based assessments — AMA",
    "The real problem with federal hiring isn't degrees, it's the timeline",
    "RIF survivors: how did you navigate the aftermath?",
    "Why does OPM still require transcripts for positions that don't need them?",
    "Federal hiring managers: do you actually care about degrees?",
    "Career change at 40 — can I get into federal service?",
    "The GS pay scale doesn't reflect skills-based value at all",
    "My agency is using AI to screen resumes now — anyone else?",
    "Opportunity@Work's research on STARs is eye-opening",
    "Should the federal government adopt skills-based hiring like the private sector?",
    "How do coding bootcamp grads fare in federal IT hiring?",
    "Veterans preference + skills-based hiring = the future?",
    "HHS just restructured — anyone know what's happening with hiring?",
    "Federal HR specialists: what's your take on removing degree requirements?",
    "I've been a GS-13 for 8 years with no degree — AMA",
    "New OPM memo on skills assessments — this is big",
    "RIF layoffs are devastating our institutional knowledge",
    "The case for paying federal employees based on skills, not grades",
    "Are competency-based interviews replacing KSAs?",
    "Just finished a federal apprenticeship — here's my experience",
    "Why do some agencies still require a Master's for GS-11?",
    "Federal hiring reform is long overdue — here's what I'd change",
    "Has anyone used the new pathways program without a degree?",
    "DOGE workforce reductions are targeting the wrong people",
    "Skills taxonomies: how should agencies define competencies?",
    "The federal workforce is aging out — skills-based hiring is the answer",
    "My hiring panel just started using structured interviews — finally!",
    "Degree requirements are a proxy for class, not competence",
    "What certifications actually matter for federal jobs?",
    "Is the Schedule A hiring authority being used for skills-based roles?",
    "Federal telework policies are driving away skilled workers",
    "How do you prove 'specialized experience' without a traditional career path?",
    "The bipartisan push for skills-based hiring — will it stick?",
    "Federal hiring freezes keep blocking real reform",
    "I'm a STAR who made it to SES — proof the system can work",
    "Should federal internships require college enrollment?",
    "Our classification system is from the 1940s — time for an overhaul",
    "Skills-based hiring won't work until we fix position classification",
]

POST_BODY_SENTENCES = [
    "I've been in federal service for {years} years and the hiring process hasn't changed much.",
    "Our agency just posted a GS-{gs} position that explicitly says 'degree OR equivalent experience.'",
    "I came from the private sector where nobody cared about my degree, and now I'm struggling with USAJobs.",
    "The recent executive order on skills-based hiring is a step in the right direction, but implementation is going to be tough.",
    "My supervisor told me they had to fight HR just to remove the degree requirement from our latest posting.",
    "I've seen incredibly talented people get screened out because they don't have a bachelor's degree.",
    "Skills-based hiring isn't just about removing degree requirements — it's about rethinking how we assess candidates entirely.",
    "The federal government loses so many good candidates to the private sector because the hiring process takes 6-9 months.",
    "I know several STARs (Skilled Through Alternative Routes) who are better at their jobs than colleagues with advanced degrees.",
    "OPM needs to update the qualification standards — many of them reference degrees that aren't even relevant anymore.",
    "The RIF process is brutal and seems to penalize newer employees regardless of their actual skills or contributions.",
    "Competency-based assessments would fix a lot of the problems with self-certification questionnaires.",
    "I've been coaching people through the federal hiring process for {years} years and the biggest barrier is always the degree requirement.",
    "The Opportunity@Work research shows that over 70 million workers in the US are STARs — the federal government should tap into that talent pool.",
    "My agency piloted skills assessments last year and the quality of our hires improved dramatically.",
    "I went through a RIF in 2024 and it was the most stressful experience of my career.",
    "Federal HR needs to stop treating degrees as a proxy for competence.",
    "The DOGE-driven workforce reductions are going to set back federal hiring reform by years.",
    "I've hired dozens of people in my career and I can tell you that a degree tells me almost nothing about job performance.",
    "The GS classification system desperately needs to incorporate skills-based elements.",
    "We lost three of our best analysts in the last RIF because they were the most junior, not the least skilled.",
    "If the private sector can move to skills-based hiring, there's no reason the federal government can't.",
    "My team has been using structured interviews with skills-based rubrics and our retention rates have improved significantly.",
    "The problem isn't just degrees — it's that federal job announcements are written in incomprehensible bureaucratic language.",
    "I've seen the same position classified at GS-9 in one agency and GS-13 in another — the system is broken.",
    "Skills-based hiring would particularly benefit veterans who have incredible real-world experience but may not have traditional credentials.",
    "The federal apprenticeship programs are a great model for skills-based entry, but they need to be scaled up.",
    "I'm worried that the push for AI resume screening will just automate the existing biases in the system.",
    "Our union is actually supportive of skills-based hiring as long as it doesn't undermine seniority protections.",
    "The biggest misconception about skills-based hiring is that it lowers standards — it actually raises them by focusing on what matters.",
    "I transitioned from a trade job to federal IT and the hardest part was translating my experience into federal resume language.",
    "HHS is going through massive changes right now and it's not clear how hiring reform fits into the picture.",
    "The data on skills-based hiring outcomes is really promising — agencies that adopt it see better diversity and performance metrics.",
    "I think we need to separate the discussion about RIFs from the discussion about hiring reform — they're related but different problems.",
    "Federal employees who got RIF'd should get priority consideration through a skills-matching program, not just bumping rights.",
    "My experience going through the Pathways program showed me how much the federal government values credentials over capability.",
    "The tech industry has been moving away from degree requirements for years — Google, Apple, IBM all dropped them.",
    "I'm a hiring manager and I wish I could post positions based purely on demonstrated skills, but OPM standards won't let me.",
    "The recent layoffs feel targeted at specific demographics rather than based on actual performance or skills assessments.",
    "Certification programs like CompTIA, PMP, and SHRM should carry more weight in federal qualification standards.",
    "I built my entire career through self-study and on-the-job learning, and I'm now a GS-{gs} making more than most of my degreed colleagues.",
    "The federal government needs to invest in upskilling current employees, not just reforming external hiring.",
    "Skills-based hiring is especially important for cybersecurity roles where the field evolves faster than any degree program can keep up.",
    "I've read the Opportunity@Work reports and the data is compelling — STARs perform just as well as workers with degrees.",
    "The problem with federal hiring reform is that every administration starts over instead of building on what worked before.",
    "RIF procedures need to factor in critical skills retention, not just tenure and veterans preference.",
    "I mentored a young person who had amazing data analytics skills but couldn't get past the HR screen because of the degree filter.",
    "The biggest win for skills-based hiring would be updating the General Schedule qualification standards across all series.",
    "Our agency created a skills inventory for all employees last year and discovered incredible untapped talent.",
    "Federal hiring timelines destroy any goodwill that skills-based posting generates — by the time we make an offer, candidates have moved on.",
]

COMMENT_BODY_SENTENCES = [
    "This is exactly my experience too.",
    "I've been saying this for years — the federal hiring system is fundamentally broken.",
    "Great post. I'd add that the timeline issue is just as important as the degree requirements.",
    "As a hiring manager, I can confirm that we lose great candidates to the private sector constantly.",
    "The skills-based approach works in theory, but HR classification specialists often push back.",
    "I went through a RIF last year and ended up in a much better position. Don't give up.",
    "OPM needs to lead on this, not just issue guidance and hope agencies comply.",
    "Totally agree. My agency just removed degree requirements for our entire IT series.",
    "The problem is that 'specialized experience' is often just code for 'has a degree.'",
    "I'm a STAR and I've been a top performer for {years} years. Degrees don't determine competence.",
    "This is such an important conversation. Federal hiring reform has bipartisan support for a reason.",
    "The real question is whether skills-based hiring survives the next administration change.",
    "I'd recommend looking into the recent OPM technical assistance materials on this.",
    "Same situation at my agency. We lost our best people in the RIF while keeping underperformers with more seniority.",
    "Has anyone actually seen the quality of hires improve after switching to skills-based assessments?",
    "The federal government employs over 2 million people — even small improvements in hiring practices have huge impacts.",
    "I used to work in private sector HR and the contrast with federal hiring is staggering.",
    "Skills-based hiring is meaningless if the pay scale doesn't reflect market value for those skills.",
    "This tracks with the research from Opportunity@Work and other organizations studying STARs.",
    "I think the apprenticeship model is the most promising pathway for non-degree candidates.",
    "My team just hired someone through a skills assessment pilot and they're one of our best performers.",
    "The DOGE cuts are making this even more urgent — we need to retain the skills we have left.",
    "Counterpoint: some positions genuinely require advanced education and we shouldn't throw the baby out with the bathwater.",
    "Federal HR needs more training on how to evaluate non-traditional credentials.",
    "I went from enlisted military to GS-{gs} with no degree. The system can work, but it's harder than it should be.",
    "Structured interviews were a game-changer for our hiring panel. Much more equitable.",
    "The data from agencies that have piloted this is really encouraging.",
    "I'm in a STEM field and even here, practical skills matter more than coursework.",
    "This is why I left federal service — the bureaucracy around hiring and promotion was suffocating.",
    "Skills taxonomies like the ones NICE and OPM are developing could standardize this across agencies.",
    "RIF procedures are governed by law, not just regulation — changing them requires Congressional action.",
    "I know several people who were RIF'd and are now making more money in the private sector. Silver lining, I guess.",
    "The real barrier isn't policy — it's culture. Hiring managers need to believe in skills-based approaches.",
    "My agency's HR office still thinks removing degree requirements will lower the quality of applicants.",
    "If you're going through a RIF, document everything and contact your union rep immediately.",
    "Skills-based hiring + remote work could transform the geographic diversity of the federal workforce.",
    "I'm cautiously optimistic. The bipartisan STARS Act could be a real turning point.",
    "Everyone talks about skills-based hiring but nobody talks about skills-based promotion.",
    "The GS system was designed for a different era. Time to modernize.",
    "I appreciate this post. Sometimes it feels like we're shouting into the void on these issues.",
    "The irony is that federal HR specialists themselves often don't have HR degrees.",
    "Coming from healthcare into federal service, the skills translation was the hardest part.",
    "This is a systemic issue. Individual agencies can only do so much without OPM reform.",
    "I've been following the Opportunity@Work research closely and it's changing how I think about hiring.",
    "If we're serious about equity in federal hiring, skills-based approaches are essential.",
    "The biggest gap I see is in mid-career transitions. The system doesn't know what to do with career changers.",
    "Federal hiring reform needs champions at the SES level to actually move the needle.",
    "I've worked in three different agencies and the hiring culture varies wildly between them.",
    "Thank you for sharing your experience. These conversations are how we build momentum for change.",
    "The federal workforce planning data is clear: we need new approaches to attract and retain talent.",
]


# -- helper: build a body paragraph from sentence templates --------------------
def _fill_template(sentence):
    """Replace tiny template tokens with random values."""
    return sentence.format(
        years=random.randint(2, 25),
        gs=random.choice([5, 7, 9, 11, 12, 13, 14, 15]),
    )


def make_body(pool, min_s=2, max_s=5):
    n = random.randint(min_s, max_s)
    chosen = random.sample(pool, k=min(n, len(pool)))
    return " ".join(_fill_template(s) for s in chosen)


# ==============================================================================
#  MAIN GENERATION LOGIC
# ==============================================================================

rows = []

n_posts = int(N_ROWS * POST_FRAC)
n_comments = N_ROWS - n_posts

# -- generate posts ------------------------------------------------------------
thread_ids = []

for _ in range(n_posts):
    tid = reddit_id()
    thread_ids.append(tid)
    rows.append({
        "type": "post",
        "thread_id": tid,
        "id": tid,
        "title": random.choice(POST_TITLES),
        "body": make_body(POST_BODY_SENTENCES),
        "created_utc": random_date(),
        "score": random_score(),
        "subreddit": random.choice(SUBREDDITS),
        "author": make_username(),
    })

# -- generate comments ---------------------------------------------------------
for _ in range(n_comments):
    parent_tid = random.choice(thread_ids)
    cid = reddit_id()
    rows.append({
        "type": "comment",
        "thread_id": parent_tid,
        "id": cid,
        "title": "",
        "body": make_body(COMMENT_BODY_SENTENCES),
        "created_utc": random_date(),
        "score": random_score(),
        "subreddit": random.choice(SUBREDDITS),
        "author": make_username(),
    })

# -- inject intentional duplicates ---------------------------------------------
dup_indices = random.sample(range(len(rows)), N_DUPLICATES)
for idx in dup_indices:
    rows.append(rows[idx].copy())

# -- inject empty/null bodies --------------------------------------------------
empty_indices = random.sample(range(len(rows)), N_EMPTY_BODY)
for i, idx in enumerate(empty_indices):
    rows[idx]["body"] = "" if i % 2 == 0 else np.nan

# -- inject a few out-of-range dates -------------------------------------------
outlier_indices = random.sample(range(len(rows)), len(OUTLIER_DATES))
for idx, dt in zip(outlier_indices, OUTLIER_DATES):
    rows[idx]["created_utc"] = dt

# -- shuffle rows --------------------------------------------------------------
random.shuffle(rows)

# -- build DataFrame and save --------------------------------------------------
df = pd.DataFrame(rows)
df["created_utc"] = pd.to_datetime(df["created_utc"])
df = df.sort_values("created_utc").reset_index(drop=True)

OUT_PATH = (
    "/Users/laptop/Library/CloudStorage/Dropbox/computer home/"
    "Claude-Workspace/personal projects/opportunity-at-work-portfolio/"
    "data/raw/reddit_skills_raw.csv"
)

df.to_csv(OUT_PATH, index=False)

# -- summary -------------------------------------------------------------------
print(f"Saved {len(df)} rows to:\n  {OUT_PATH}\n")
print("Schema:")
print(df.dtypes)
print(f"\nType distribution:\n{df['type'].value_counts()}")
print(f"\nSubreddit distribution:\n{df['subreddit'].value_counts()}")
print(f"\nScore stats:\n{df['score'].describe()}")
print(f"\nDate range: {df['created_utc'].min()} -> {df['created_utc'].max()}")
print(f"\nEmpty/null bodies: {df['body'].isna().sum() + (df['body'] == '').sum()}")
dup_count = df.duplicated(subset=["thread_id", "id"], keep=False).sum()
print(f"Duplicate (thread_id + id) rows: {dup_count}")
print(f"\nFirst 5 rows:\n{df.head()}")
