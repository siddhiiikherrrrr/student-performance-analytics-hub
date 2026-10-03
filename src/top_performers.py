"""Module 4 - Top Performers Analysis."""
from __future__ import annotations

import pandas as pd

from . import config as C

COLS = ["Score_Rank", "Student_ID", "Student_Name", "Gender", "Avg_Score", "Math_Score",
        "Science_Score", "English_Score", "Attendance_Percentage", "Study_Hours"]


def analyze(df: pd.DataFrame, n: int = 10) -> dict:
    top_overall = df.sort_values(["Score_Rank", "Student_ID"]).head(n)[COLS].reset_index(drop=True)

    parts = []
    for col in C.SUBJECTS:
        t = df.nlargest(5, col)[["Student_ID", "Student_Name", col]].copy()
        t.insert(0, "Subject", col.replace("_Score", ""))
        t.insert(1, "Rank_In_Subject", range(1, len(t) + 1))
        parts.append(t.rename(columns={col: "Score"}))
    top_by_subject = pd.concat(parts, ignore_index=True)

    elite = df["Performance_Tier"] == "Top 10%"
    metrics = {"Students": ("Student_ID", "count"), "Avg_Score": ("Avg_Score", "mean"),
               "Avg_Attendance": ("Attendance_Percentage", "mean"), "Avg_Study_Hours": ("Study_Hours", "mean"),
               "Study_Efficiency": ("Study_Efficiency", "mean")}
    profile = (df.assign(Group=elite.map({True: "Top 10%", False: "Everyone else"}))
               .groupby("Group").agg(**metrics).round(1).reset_index())
    profile["Female_%"] = df.assign(Group=elite.map({True: "Top 10%", False: "Everyone else"})) \
        .groupby("Group")["Gender"].apply(lambda s: (s == "Female").mean() * 100).round(1).values

    upper = df[df["Percentile"] >= 75]
    efficient = (upper[upper["Study_Hours"] <= df["Study_Hours"].median()]
                 .sort_values("Study_Efficiency", ascending=False).head(n)
                 [["Student_ID", "Student_Name", "Avg_Score", "Study_Hours", "Study_Efficiency"]]
                 .reset_index(drop=True))
    return {"top_overall": top_overall, "top_by_subject": top_by_subject,
            "profile": profile, "efficient_learners": efficient, "elite_count": int(elite.sum())}
