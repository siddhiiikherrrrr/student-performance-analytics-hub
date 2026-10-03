"""Assemble reports/analysis_report.md from computed results (no hand-typed numbers)."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from . import config as C


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    d = df.head(max_rows) if max_rows else df
    d = d.copy()
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].map(lambda v: f"{v:,.1f}")
    head = "| " + " | ".join(map(str, d.columns)) + " |"
    sep = "|" + "|".join("---" for _ in d.columns) + "|"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in d.itertuples(index=False)]
    return "\n".join([head, sep, *body])


def build(students, qa, kpis, att, subj, top, risk, insights, path: Path) -> None:
    rel = "figures"
    bullets = "\n".join(f"- **{r.Category}** ({r.Severity}): {r.Insight}"
                        for r in insights[insights.Category != "Recommendation"].itertuples())
    recs = "\n".join(f"{i}. {r.Insight}" for i, r in
                     enumerate(insights[insights.Category == "Recommendation"].itertuples(), 1))
    kpi_tbl = md_table(pd.DataFrame({"KPI": kpis.keys(), "Value": [str(v) for v in kpis.values()]}))

    text = f"""# Student Performance Analysis Report

*Generated {date.today():%d %B %Y} by the Student Performance Analytics Hub - dataset is synthetic.*

## 1. Executive summary

{kpi_tbl}

**What the data says**

{bullets}

**Recommended actions**

{recs}

## 2. Data quality

The raw file contained **{qa['rows_in']} rows**; the cleaning module produced **{qa['rows_out']}** analysis-ready records
(completeness {qa['completeness_after_%']}%).

| Check | Result |
|---|---|
| Duplicate Student_IDs removed | {qa['duplicates_removed']} |
| Names standardised (case/whitespace) | {qa['names_standardised']} |
| Gender labels normalised | {qa['gender_labels_fixed']} |
| Impossible values nullified | {sum(qa['out_of_range_nullified'].values())} |
| Rows with imputed values | {qa['rows_imputed']} |

Missing values were filled with the column **median** and every affected row carries `Was_Imputed = True`
so it can be filtered out of sensitive analysis.

## 3. Attendance analysis

Mean attendance is **{att['summary']['avg_attendance']}%** (median {att['summary']['median_attendance']}%).
**{att['summary']['chronic_absentees']} students ({att['summary']['chronic_absentee_pct']}%)** fall below the
{C.ATTENDANCE_THRESHOLD}% threshold, and attendance correlates with results at
**r = {att['summary']['corr_with_score']}**.

{md_table(att['bands'])}

![Score by attendance band]({rel}/attendance_bands.png)

![Attendance vs performance]({rel}/attendance_vs_score.png)

## 4. Subject-wise performance

{md_table(subj['summary'])}

Gender comparison (mean score):

{md_table(subj['by_gender'])}

Score distribution by band:

{md_table(subj['distribution'])}

![Subject performance]({rel}/subject_performance.png)

![Score distribution]({rel}/score_distribution.png)

## 5. Top performers

{md_table(top['top_overall'])}

How the top 10% differ from everyone else:

{md_table(top['profile'])}

Efficient learners (upper quartile, at-or-below-median study time):

{md_table(top['efficient_learners'], 5)}

## 6. Risk detection

Risk is scored 0-100 from attendance, average score, failed subjects and study time
(see `src/risk_detection.py`).

{md_table(risk['distribution'])}

Primary driver among flagged (High + Medium) students:

{md_table(risk['drivers'])}

Ten highest-risk students:

{md_table(risk['watchlist'][['Student_ID','Student_Name','Attendance_Percentage','Avg_Score','Risk_Score','Risk_Level','Recommended_Action']], 10)}

![Risk distribution]({rel}/risk_distribution.png)

## 7. Method and limitations

- Pass mark {C.PASS_MARK}; distinction {C.DISTINCTION_MARK}; chronic absence < {C.ATTENDANCE_THRESHOLD}% (all configurable in `src/config.py`).
- Correlations describe association, not causation; attendance and study time are also linked to unmeasured factors.
- The risk model is a transparent screening tool. It should prompt a conversation, not replace teacher judgement.
- Data is synthetic and generated for demonstration; do not draw real-world conclusions from it.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
