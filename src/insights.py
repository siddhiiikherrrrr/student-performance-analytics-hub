"""Module 6 - Performance Insights Generator.

Rule-based narrative engine: every sentence is computed from the data, so the
text stays correct whenever the dataset changes.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


def _slope(x: pd.Series, y: pd.Series) -> float:
    return float(np.polyfit(x, y, 1)[0])


def generate(df: pd.DataFrame, qa: dict | None = None) -> pd.DataFrame:
    rows: list[tuple[str, str, str]] = []
    add = lambda cat, sev, msg: rows.append((cat, sev, msg))
    n = len(df)

    # cohort snapshot
    pass_rate = df["All_Subjects_Passed"].mean() * 100
    add("Overview", "Info", f"{n} students average {df['Avg_Score'].mean():.1f}/100 across three subjects; "
        f"{pass_rate:.1f}% pass every subject (pass mark {C.PASS_MARK}).")

    # attendance -> score
    r = df["Attendance_Percentage"].corr(df["Avg_Score"])
    per10 = _slope(df["Attendance_Percentage"], df["Avg_Score"]) * 10
    add("Attendance", "Warning" if r > 0.3 else "Info",
        f"Attendance is a strong lever: every extra 10 percentage points is associated with about "
        f"{per10:+.1f} marks on the average score (r = {r:.2f}).")
    low = df[df["Attendance_Percentage"] < C.ATTENDANCE_THRESHOLD]
    ok = df[df["Attendance_Percentage"] >= C.ATTENDANCE_THRESHOLD]
    if len(low):
        add("Attendance", "Critical" if len(low) / n > 0.2 else "Warning",
            f"{len(low)} students ({len(low) / n * 100:.1f}%) attend under {C.ATTENDANCE_THRESHOLD}% of classes "
            f"and score {ok['Avg_Score'].mean() - low['Avg_Score'].mean():.1f} marks lower on average "
            f"({low['Avg_Score'].mean():.1f} vs {ok['Avg_Score'].mean():.1f}).")

    # study hours
    hi, lo = df[df["Study_Hours"] >= 5], df[df["Study_Hours"] < 3]
    if len(hi) and len(lo):
        add("Study Habits", "Info",
            f"Students studying 5+ hours/day average {hi['Avg_Score'].mean():.1f} versus "
            f"{lo['Avg_Score'].mean():.1f} for those under 3 hours - a "
            f"{hi['Avg_Score'].mean() - lo['Avg_Score'].mean():.1f}-mark gap "
            f"({_slope(df['Study_Hours'], df['Avg_Score']):+.1f} marks per extra study hour).")

    # subjects
    means = df[C.SUBJECTS].mean().rename(lambda s: s.replace("_Score", ""))
    passes = (df[C.SUBJECTS] >= C.PASS_MARK).mean().mul(100).rename(lambda s: s.replace("_Score", ""))
    add("Subjects", "Warning" if passes.min() < 85 else "Info",
        f"{means.idxmax()} is the strongest subject ({means.max():.1f} avg); {means.idxmin()} is the weakest "
        f"({means.min():.1f} avg, {passes[means.idxmin()]:.1f}% pass rate).")

    # gender gaps
    known = df[df["Gender"].isin(["Male", "Female"])]
    gaps = {s.replace("_Score", ""): known[known.Gender == "Female"][s].mean() - known[known.Gender == "Male"][s].mean()
            for s in C.SUBJECTS}
    big = {s: g for s, g in gaps.items() if abs(g) >= 2}
    if big:
        txt = ", ".join(f"{s} ({'girls' if g > 0 else 'boys'} +{abs(g):.1f})" for s, g in big.items())
        add("Equity", "Info", f"Gender gaps of 2+ marks appear in: {txt}. Consider subject-specific engagement work.")
    else:
        add("Equity", "Positive", "No subject shows a gender gap larger than 2 marks.")

    # risk
    at_risk = df[df["Risk_Level"] != "Low"]
    hi_risk = int((df["Risk_Level"] == "High").sum())
    if len(at_risk):
        top_driver = at_risk["Primary_Risk_Driver"].value_counts()
        add("Risk", "Critical" if hi_risk / n > 0.05 else "Warning",
            f"{len(at_risk)} students ({len(at_risk) / n * 100:.1f}%) need attention - {hi_risk} High risk. "
            f"The most common primary driver is {top_driver.index[0].lower()} "
            f"({top_driver.iloc[0]} students).")

    # top performers
    elite = df[df["Performance_Tier"] == "Top 10%"]
    rest = df[df["Performance_Tier"] != "Top 10%"]
    add("Top Performers", "Positive",
        f"The top 10% ({len(elite)} students) average {elite['Avg_Score'].mean():.1f} with "
        f"{elite['Attendance_Percentage'].mean():.1f}% attendance and {elite['Study_Hours'].mean():.1f} study hours/day, "
        f"versus {rest['Attendance_Percentage'].mean():.1f}% and {rest['Study_Hours'].mean():.1f}h for everyone else.")
    eff = df[(df["Percentile"] >= 75) & (df["Study_Hours"] <= df["Study_Hours"].median())]
    if len(eff):
        add("Top Performers", "Positive",
            f"{len(eff)} upper-quartile students achieve results on at-or-below-median study time - "
            "worth interviewing for study-technique best practice.")

    # data quality
    if qa:
        add("Data Quality", "Info",
            f"Cleaning removed {qa['duplicates_removed']} duplicate records and repaired "
            f"{qa['rows_imputed']} rows with missing or invalid values (median imputation, flagged in Was_Imputed).")

    # recommendations
    add("Recommendation", "Action",
        f"Launch an attendance recovery programme for the {len(low)} students below {C.ATTENDANCE_THRESHOLD}% - "
        "the largest and cheapest lever on results.")
    if len(at_risk):
        add("Recommendation", "Action",
            f"Assign mentors to the {hi_risk} High-risk students this week and review the {len(at_risk) - hi_risk} "
            "Medium-risk students in the next fortnightly meeting.")
    add("Recommendation", "Action",
        f"Run targeted {means.idxmin()} revision clinics, and use top performers as peer tutors.")

    out = pd.DataFrame(rows, columns=["Category", "Severity", "Insight"])
    out.insert(0, "Id", range(1, len(out) + 1))
    return out
