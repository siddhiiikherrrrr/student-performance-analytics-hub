# Student Performance Analysis Report

*Generated 28 September 2026 by the Student Performance Analytics Hub - dataset is synthetic.*

## 1. Executive summary

| KPI | Value |
|---|---|
| Total Students | 492 |
| Average Score | 64.2 |
| Average Attendance | 82.4% |
| Average Study Hours | 3.8 |
| Pass Rate (all subjects) | 92.7% |
| Chronic Absentees | 101 |
| At-Risk Students (High+Medium) | 101 |
| High-Risk Students | 39 |
| Top Performers (Top 10%) | 50 |

**What the data says**

- **Overview** (Info): 492 students average 64.2/100 across three subjects; 92.7% pass every subject (pass mark 40).
- **Attendance** (Warning): Attendance is a strong lever: every extra 10 percentage points is associated with about +7.0 marks on the average score (r = 0.61).
- **Attendance** (Critical): 101 students (20.5%) attend under 75% of classes and score 13.4 marks lower on average (53.5 vs 66.9).
- **Study Habits** (Info): Students studying 5+ hours/day average 75.4 versus 53.8 for those under 3 hours - a 21.6-mark gap (+5.5 marks per extra study hour).
- **Subjects** (Info): English is the strongest subject (64.6 avg); Science is the weakest (63.6 avg, 96.1% pass rate).
- **Equity** (Info): Gender gaps of 2+ marks appear in: English (girls +2.8). Consider subject-specific engagement work.
- **Risk** (Critical): 101 students (20.5%) need attention - 39 High risk. The most common primary driver is attendance (71 students).
- **Top Performers** (Positive): The top 10% (50 students) average 84.2 with 90.9% attendance and 5.8 study hours/day, versus 81.4% and 3.6h for everyone else.
- **Top Performers** (Positive): 11 upper-quartile students achieve results on at-or-below-median study time - worth interviewing for study-technique best practice.
- **Data Quality** (Info): Cleaning removed 8 duplicate records and repaired 44 rows with missing or invalid values (median imputation, flagged in Was_Imputed).

**Recommended actions**

1. Launch an attendance recovery programme for the 101 students below 75% - the largest and cheapest lever on results.
2. Assign mentors to the 39 High-risk students this week and review the 62 Medium-risk students in the next fortnightly meeting.
3. Run targeted Science revision clinics, and use top performers as peer tutors.

## 2. Data quality

The raw file contained **500 rows**; the cleaning module produced **492** analysis-ready records
(completeness 100.0%).

| Check | Result |
|---|---|
| Duplicate Student_IDs removed | 8 |
| Names standardised (case/whitespace) | 23 |
| Gender labels normalised | 20 |
| Impossible values nullified | 5 |
| Rows with imputed values | 44 |

Missing values were filled with the column **median** and every affected row carries `Was_Imputed = True`
so it can be filtered out of sensitive analysis.

## 3. Attendance analysis

Mean attendance is **82.4%** (median 83.9%).
**101 students (20.5%)** fall below the
75% threshold, and attendance correlates with results at
**r = 0.615**.

| Band | Students | Avg_Score | Avg_Study_Hours | Pass_Rate_% | Share_% |
|---|---|---|---|---|---|
| <60% | 16 | 50.9 | 1.8 | 62.5 | 3.3 |
| 60-75% | 85 | 54.0 | 2.7 | 80.0 | 17.3 |
| 75-85% | 166 | 61.7 | 3.4 | 93.4 | 33.7 |
| 85-95% | 179 | 69.5 | 4.6 | 98.9 | 36.4 |
| 95-100% | 46 | 75.6 | 5.3 | 100.0 | 9.3 |

![Score by attendance band](figures/attendance_bands.png)

![Attendance vs performance](figures/attendance_vs_score.png)

## 4. Subject-wise performance

| Subject | Mean | Median | Std_Dev | Min | Max | Pass_Rate_% | Distinction_Rate_% |
|---|---|---|---|---|---|---|---|
| English | 64.6 | 65.1 | 13.2 | 25.2 | 98.7 | 96.5 | 5.9 |
| Math | 64.3 | 65.2 | 12.9 | 20.4 | 95.2 | 96.7 | 5.3 |
| Science | 63.6 | 63.2 | 13.1 | 29.3 | 96.4 | 96.1 | 5.3 |

Gender comparison (mean score):

| Subject | Female | Male | Gap_F_minus_M |
|---|---|---|---|
| English | 66.1 | 63.2 | 2.9 |
| Math | 63.7 | 64.8 | -1.1 |
| Science | 63.2 | 64.0 | -0.8 |

Score distribution by band:

| Subject | Fail (<40) | 40-54 | 55-69 | 70-84 | Distinction (85+) |
|---|---|---|---|---|---|
| English | 17 | 97 | 199 | 150 | 29 |
| Math | 16 | 95 | 221 | 134 | 26 |
| Science | 19 | 108 | 203 | 136 | 26 |

![Subject performance](figures/subject_performance.png)

![Score distribution](figures/score_distribution.png)

## 5. Top performers

| Score_Rank | Student_ID | Student_Name | Gender | Avg_Score | Math_Score | Science_Score | English_Score | Attendance_Percentage | Study_Hours |
|---|---|---|---|---|---|---|---|---|---|
| 1 | STU-0362 | Navya Gupta | Female | 96.0 | 93.5 | 95.8 | 98.7 | 92.6 | 6.1 |
| 2 | STU-0078 | Dev Nair | Male | 92.3 | 89.4 | 93.3 | 94.2 | 86.5 | 5.6 |
| 3 | STU-0265 | Vanya Jain | Female | 91.7 | 91.2 | 96.4 | 87.5 | 94.1 | 6.9 |
| 4 | STU-0089 | Sneha Nair | Female | 90.7 | 94.6 | 87.6 | 89.9 | 98.0 | 7.8 |
| 5 | STU-0139 | Harsh Shah | Male | 90.5 | 95.2 | 86.9 | 89.3 | 100.0 | 6.7 |
| 6 | STU-0066 | Rohan Patel | Male | 89.4 | 92.2 | 87.6 | 88.4 | 93.1 | 3.9 |
| 7 | STU-0176 | Neel Kulkarni | Male | 88.7 | 91.8 | 89.4 | 85.0 | 87.1 | 6.3 |
| 8 | STU-0130 | Naina Menon | Female | 87.8 | 86.9 | 87.2 | 89.2 | 100.0 | 6.7 |
| 9 | STU-0095 | Pihu Chauhan | Female | 87.7 | 81.9 | 91.0 | 90.2 | 94.7 | 6.2 |
| 10 | STU-0027 | Tanmay Vora | Male | 87.5 | 90.4 | 89.2 | 83.0 | 94.4 | 6.7 |

How the top 10% differ from everyone else:

| Group | Students | Avg_Score | Avg_Attendance | Avg_Study_Hours | Study_Efficiency | Female_% |
|---|---|---|---|---|---|---|
| Everyone else | 442 | 61.9 | 81.4 | 3.6 | 21.1 | 49.5 |
| Top 10% | 50 | 84.2 | 90.9 | 5.8 | 15.1 | 46.0 |

Efficient learners (upper quartile, at-or-below-median study time):

| Student_ID | Student_Name | Avg_Score | Study_Hours | Study_Efficiency |
|---|---|---|---|---|
| STU-0006 | Trisha Bhatt | 73.4 | 2.2 | 33.4 |
| STU-0451 | Naina Vora | 73.1 | 2.3 | 31.8 |
| STU-0186 | Karan Pandey | 72.8 | 2.9 | 25.1 |
| STU-0232 | Aanya Gupta | 73.7 | 3.1 | 23.8 |
| STU-0440 | Karan Sharma | 85.8 | 3.8 | 22.6 |

## 6. Risk detection

Risk is scored 0-100 from attendance, average score, failed subjects and study time
(see `src/risk_detection.py`).

| Risk_Level | Students | Share_% | Avg_Score | Avg_Attendance | Avg_Study_Hours |
|---|---|---|---|---|---|
| High | 39 | 7.9 | 43.3 | 63.0 | 1.7 |
| Medium | 62 | 12.6 | 53.6 | 71.5 | 2.2 |
| Low | 391 | 79.5 | 67.9 | 86.0 | 4.3 |

Primary driver among flagged (High + Medium) students:

| Driver | Students |
|---|---|
| Attendance | 71 |
| Academic Score | 30 |

Ten highest-risk students:

| Student_ID | Student_Name | Attendance_Percentage | Avg_Score | Risk_Score | Risk_Level | Recommended_Action |
|---|---|---|---|---|---|---|
| STU-0222 | Aarav Kapoor | 64.7 | 25.0 | 100 | High | Escalate: attendance contract + guardian outreach |
| STU-0353 | Kabir Parekh | 62.6 | 33.1 | 100 | High | Escalate: attendance contract + guardian outreach |
| STU-0182 | Neel Mehta | 64.1 | 38.2 | 100 | High | Escalate: attendance contract + guardian outreach |
| STU-0478 | Rohan Bhatt | 51.6 | 38.3 | 100 | High | Escalate: attendance contract + guardian outreach |
| STU-0087 | Sahil Patel | 63.5 | 40.8 | 100 | High | Escalate: attendance contract + guardian outreach |
| STU-0431 | Manav Kapoor | 63.2 | 40.6 | 90 | High | Escalate: attendance contract + guardian outreach |
| STU-0422 | Trisha Reddy | 45.1 | 41.5 | 90 | High | Escalate: attendance contract + guardian outreach |
| STU-0256 | Sahil Joshi | 63.0 | 42.2 | 90 | High | Escalate: attendance contract + guardian outreach |
| STU-0357 | Harsh Trivedi | 58.2 | 43.3 | 90 | High | Escalate: attendance contract + guardian outreach |
| STU-0427 | Bhavya Singh | 62.5 | 43.8 | 90 | High | Escalate: attendance contract + guardian outreach |

![Risk distribution](figures/risk_distribution.png)

## 7. Method and limitations

- Pass mark 40; distinction 85; chronic absence < 75% (all configurable in `src/config.py`).
- Correlations describe association, not causation; attendance and study time are also linked to unmeasured factors.
- The risk model is a transparent screening tool. It should prompt a conversation, not replace teacher judgement.
- Data is synthetic and generated for demonstration; do not draw real-world conclusions from it.
