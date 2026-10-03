"""Module 2 - Attendance Analysis."""
from __future__ import annotations

import pandas as pd

from . import config as C


def analyze(df: pd.DataFrame) -> dict:
    thr = C.ATTENDANCE_THRESHOLD
    att = df["Attendance_Percentage"]

    bands = (df.groupby(["Attendance_Band_Order", "Attendance_Band"])
             .agg(Students=("Student_ID", "count"), Avg_Score=("Avg_Score", "mean"),
                  Avg_Study_Hours=("Study_Hours", "mean"), Pass_Rate=("All_Subjects_Passed", "mean"))
             .reset_index().sort_values("Attendance_Band_Order").drop(columns="Attendance_Band_Order"))
    bands["Share_%"] = bands["Students"] / len(df) * 100
    bands["Pass_Rate"] = bands["Pass_Rate"] * 100
    bands = bands.rename(columns={"Attendance_Band": "Band", "Pass_Rate": "Pass_Rate_%"}).round(1)

    by_gender = (df.groupby("Gender")
                 .agg(Students=("Student_ID", "count"), Avg_Attendance=("Attendance_Percentage", "mean"),
                      Avg_Score=("Avg_Score", "mean"),
                      Chronic_Absentees=("Attendance_Percentage", lambda s: int((s < thr).sum())))
                 .reset_index().round(1))

    cols = ["Student_ID", "Student_Name", "Gender", "Attendance_Percentage", "Avg_Score", "Risk_Level"]
    chronic = df.loc[att < thr, [c for c in cols if c in df.columns]].sort_values("Attendance_Percentage")

    return {
        "summary": {
            "avg_attendance": round(att.mean(), 1), "median_attendance": round(att.median(), 1),
            "chronic_absentees": int((att < thr).sum()),
            "chronic_absentee_pct": round((att < thr).mean() * 100, 1),
            "excellent_attendance_pct": round((att >= 95).mean() * 100, 1),
            "corr_with_score": round(att.corr(df["Avg_Score"]), 3),
        },
        "bands": bands, "by_gender": by_gender, "chronic_absentees": chronic,
    }
