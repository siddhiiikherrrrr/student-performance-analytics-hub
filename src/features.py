"""Feature engineering shared by every analysis module."""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    subj = d[C.SUBJECTS]
    d["Total_Score"] = subj.sum(axis=1).round(1)
    d["Avg_Score"] = subj.mean(axis=1).round(1)
    d["Subject_Std"] = subj.std(axis=1).round(1)
    d["Grade"] = pd.cut(d["Avg_Score"], C.GRADE_BINS, labels=C.GRADE_LABELS, right=False).astype(str)

    att_band = pd.cut(d["Attendance_Percentage"], C.ATTENDANCE_BINS, labels=C.ATTENDANCE_LABELS, right=False)
    d["Attendance_Band"] = att_band.astype(str)
    d["Attendance_Band_Order"] = att_band.cat.codes + 1
    d["Study_Band"] = pd.cut(d["Study_Hours"], C.STUDY_BINS, labels=C.STUDY_LABELS, right=False).astype(str)

    d["Best_Subject"] = subj.idxmax(axis=1).str.replace("_Score", "", regex=False)
    d["Weakest_Subject"] = subj.idxmin(axis=1).str.replace("_Score", "", regex=False)
    d["Failing_Subjects"] = (subj < C.PASS_MARK).sum(axis=1)
    d["All_Subjects_Passed"] = d["Failing_Subjects"] == 0

    d["Score_Rank"] = d["Avg_Score"].rank(ascending=False, method="min").astype(int)
    d["Percentile"] = (d["Avg_Score"].rank(pct=True) * 100).round(1)
    d["Performance_Tier"] = pd.cut(d["Percentile"], [0, 25, 75, 90, 100.01],
                                   labels=["Lower Quartile", "Mid Range", "Upper Quartile", "Top 10%"],
                                   right=False).astype(str)
    d["Study_Efficiency"] = (d["Avg_Score"] / d["Study_Hours"].replace(0, np.nan)).round(1)
    return d


def to_long(df: pd.DataFrame) -> pd.DataFrame:
    """One row per student-subject: ideal for Power BI subject visuals."""
    keep = ["Student_ID", "Student_Name", "Gender", "Attendance_Band", "Attendance_Band_Order",
            "Risk_Level", "Performance_Tier"]
    keep = [c for c in keep if c in df.columns]
    long = df.melt(id_vars=keep, value_vars=C.SUBJECTS, var_name="Subject", value_name="Score")
    long["Subject"] = long["Subject"].str.replace("_Score", "", regex=False)
    long["Passed"] = long["Score"] >= C.PASS_MARK
    long["Distinction"] = long["Score"] >= C.DISTINCTION_MARK
    return long
