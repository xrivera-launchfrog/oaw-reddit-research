# Survey Design: Teacher Professional Development Effectiveness

## Survey Metadata

| Field | Detail |
|-------|--------|
| **Title** | Teacher Professional Development Effectiveness Survey |
| **Purpose** | Assess the perceived impact and quality of professional development programs on teaching practice, with a focus on identifying which PD formats and topics best support classroom outcomes |
| **Target Respondents** | K-12 teachers who participated in at least one PD session in the current school year |
| **Distribution Method** | SurveyMonkey (email invitation with unique links per school) |
| **Estimated Completion Time** | 8–10 minutes |
| **Response Goal** | 300 responses across 15 partner schools |
| **IRB Status** | Exempt — survey collects no PII beyond school name and role |

---

## Survey Sections

### Section 1: Demographics & Context (5 questions)

**Q1.** What grade band do you primarily teach?
- *Type:* Multiple choice (single select)
- *Options:* Pre-K–2 / 3–5 / 6–8 / 9–12

**Q2.** How many years have you been teaching?
- *Type:* Multiple choice (single select)
- *Options:* 0–2 years / 3–5 years / 6–10 years / 11–20 years / 20+ years

**Q3.** What subject area(s) do you teach?
- *Type:* Multiple choice (multi-select)
- *Options:* ELA / Math / Science / Social Studies / Special Education / Electives/Arts / Other (specify)

**Q4.** Which school do you teach at?
- *Type:* Dropdown (pre-populated with partner school names)
- *Skip logic:* None

**Q5.** How many PD sessions did you attend this school year?
- *Type:* Multiple choice (single select)
- *Options:* 1–2 / 3–5 / 6–10 / More than 10

---

### Section 2: PD Experience & Format (4 questions)

**Q6.** Which PD formats have you participated in this year? (Select all that apply)
- *Type:* Multiple choice (multi-select)
- *Options:* In-person workshop / Virtual workshop / Coaching or mentoring / Peer observation / Self-paced online course / Conference or summit / Professional learning community (PLC)

**Q7.** Which format was MOST valuable to your teaching practice?
- *Type:* Multiple choice (single select)
- *Options:* Same as Q6
- *Skip logic:* Only shows options selected in Q6

**Q8.** What PD topics were most relevant to your current needs? (Select up to 3)
- *Type:* Multiple choice (multi-select, max 3)
- *Options:* Culturally responsive teaching / Data-driven instruction / Classroom management / Curriculum design / Technology integration / Social-emotional learning / Differentiated instruction / Assessment strategies / Other (specify)

**Q9.** How well did PD sessions align with your school's instructional priorities?
- *Type:* Likert scale (5-point)
- *Scale:* Not at all aligned / Slightly aligned / Moderately aligned / Very aligned / Perfectly aligned

---

### Section 3: Impact on Practice (5 questions)

**Q10.** After attending PD, how often did you implement new strategies in your classroom?
- *Type:* Likert scale (5-point)
- *Scale:* Never / Rarely / Sometimes / Often / Almost always

**Q11.** To what extent did PD improve your confidence in the following areas?
- *Type:* Matrix / Likert grid (5-point: No improvement → Significant improvement)
- *Rows:* Subject content knowledge / Instructional strategies / Student engagement techniques / Assessment and feedback / Differentiating for diverse learners

**Q12.** Did you observe measurable changes in student outcomes (engagement, assessment scores, behavior) after implementing PD strategies?
- *Type:* Multiple choice (single select)
- *Options:* Yes, clearly / Somewhat / Not sure / No / Not applicable
- *Skip logic:* If "Yes, clearly" or "Somewhat" → show Q13

**Q13.** Briefly describe one change in student outcomes you observed.
- *Type:* Open-ended (text box, 500 character limit)
- *Skip logic:* Only shown if Q12 = "Yes, clearly" or "Somewhat"

**Q14.** How likely are you to recommend the PD you received to a colleague?
- *Type:* Net Promoter Score (0–10 scale)
- *Scale:* 0 = Not at all likely / 10 = Extremely likely

---

### Section 4: Barriers & Suggestions (3 questions)

**Q15.** What barriers, if any, prevented you from fully engaging with PD this year? (Select all that apply)
- *Type:* Multiple choice (multi-select)
- *Options:* Scheduling conflicts / Content not relevant to my role / Lack of follow-up or coaching / Too many competing priorities / PD was too theoretical / not practical / Technology issues (for virtual PD) / No significant barriers / Other (specify)

**Q16.** What ONE change would most improve PD at your school?
- *Type:* Open-ended (text box, 500 character limit)

**Q17.** Any additional comments about your PD experience this year?
- *Type:* Open-ended (text box, 1000 character limit)
- *Required:* No

---

## Implementation Notes

### Distribution Plan
1. Survey link emailed to school-based PD coordinators for forwarding
2. Unique collector link per school to enable school-level analysis without collecting PII
3. Two reminder emails: 5 days and 10 days after initial send
4. Survey open for 3 weeks

### Analysis Plan
- Descriptive statistics for all closed-ended questions
- Cross-tabulation by grade band, experience level, and school
- NPS calculation and segmentation (promoters/passives/detractors)
- Thematic coding of open-ended responses (Q13, Q16, Q17)
- Report delivered as slide deck + data appendix

### SurveyMonkey Configuration
- Use "Question Skip Logic" for Q7 (conditional on Q6) and Q13 (conditional on Q12)
- Enable "Anonymous Responses" collector setting
- Set Q1–Q12 and Q14–Q16 as required; Q13 and Q17 as optional
- Apply Leading Educators branding (logo, brand colors) to survey theme
