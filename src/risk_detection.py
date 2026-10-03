"""Module 5 - Risk Student Detection.

A transparent, points-based early-warning model (0-100). Every point is traceable
to a rule in config.py, so a teacher can see *why* a student is flagged.

  Attendance      <65% = 35 | <75% = 20
  Academic avg    <45  = 35 | <55  = 20 | <65 = 8
  Failed subjects 10 pts each (max 20)
  Study habits    <2h  = 10 | <3h  = 5

Level: High >= 60, Medium >= 30, otherwise Low.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C

DRIVERS = np.array(["Attendance", "Academic Score", "Subject Failures", "Study Habits"])
DRIVER_ACTION = {"Attendance": "attendance contract + guardian outreach",
                 "Academic Score": "structured tutoring plan",
                 "Subject Failures": "subject-specific remediation",
                 "Study Habits": "study-skills coaching"}


def _factors(r: pd.Series) -> str:
    out = []
    if r["Attendance_Percentage"] < C.ATTENDANCE_THRESHOLD:
        out.append(f"Low attendance ({r['Attendance_Percentage']:.0f}%)")
    if r["Avg_Score"] < 55:
        out.append(f"Low average ({r['Avg_Score']:.1f})")
    if r["Failing_Subjects"] > 0:
        failed = [s.replace("_Score", "") for s in C.SUBJECTS if r[s] < C.PASS_MARK]
        out.append("Failing " + "/".join(failed))
    if r["Study_Hours"] < 3:
        out.append(f"Low study time ({r['Study_Hours']:.1f}h)")
    return "; ".join(out) if out else "None"


def assess(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    att, avg, hrs = d["Attendance_Percentage"], d["Avg_Score"], d["Study_Hours"]
    pts = np.column_stack([
        np.select([att < 65, att < C.ATTENDANCE_THRESHOLD], [35, 20], 0),
        np.select([avg < 45, avg < 55, avg < 65], [35, 20, 8], 0),
        np.minimum(d["Failing_Subjects"].to_numpy() * 10, 20),
        np.select([hrs < 2, hrs < 3], [10, 5], 0),
    ])
    d["Risk_Score"] = np.minimum(pts.sum(axis=1), 100)
    d["Risk_Level"] = pd.cut(d["Risk_Score"], [-np.inf, C.RISK_MEDIUM_CUTOFF, C.RISK_HIGH_CUTOFF, np.inf],
                             labels=["Low", "Medium", "High"], right=False).astype(str)
    d["Risk_Level_Order"] = d["Risk_Level"].map({"High": 1, "Medium": 2, "Low": 3})
    d["Primary_Risk_Driver"] = np.where(pts.max(axis=1) == 0, "None", DRIVERS[pts.argmax(axis=1)])
    d["Risk_Factors"] = d.apply(_factors, axis=1)

    prefix = {"High": "Escalate", "Medium": "Support"}
    d["Recommended_Action"] = [
        "Monitor" if lvl == "Low" else f"{prefix[lvl]}: {DRIVER_ACTION[drv]}"
        for lvl, drv in zip(d["Risk_Level"], d["Primary_Risk_Driver"])]
    return d


def analyze(df: pd.DataFrame) -> dict:
    order = ["High", "Medium", "Low"]
    dist = (df.groupby("Risk_Level").agg(Students=("Student_ID", "count"), Avg_Score=("Avg_Score", "mean"),
                                         Avg_Attendance=("Attendance_Percentage", "mean"),
                                         Avg_Study_Hours=("Study_Hours", "mean"))
            .reindex(order).fillna(0).round(1).reset_index())
    dist.insert(2, "Share_%", (dist["Students"] / len(df) * 100).round(1))

    flagged = df[df["Risk_Level"] != "Low"]
    drivers = (flagged["Primary_Risk_Driver"].value_counts().rename_axis("Driver")
               .reset_index(name="Students"))
    cols = ["Student_ID", "Student_Name", "Gender", "Attendance_Percentage", "Avg_Score", "Study_Hours",
            "Risk_Score", "Risk_Level", "Primary_Risk_Driver", "Risk_Factors", "Recommended_Action"]
    watchlist = (flagged.sort_values(["Risk_Score", "Avg_Score"], ascending=[False, True])[cols]
                 .reset_index(drop=True))
    return {"distribution": dist, "drivers": drivers, "watchlist": watchlist,
            "high": int((df["Risk_Level"] == "High").sum()),
            "medium": int((df["Risk_Level"] == "Medium").sum())}
