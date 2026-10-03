"""Module 3 - Subject-wise Performance Analysis."""
from __future__ import annotations

import pandas as pd

from . import config as C
from .features import to_long


def analyze(df: pd.DataFrame) -> dict:
    long = to_long(df)
    g = long.groupby("Subject")["Score"]
    summary = pd.DataFrame({
        "Mean": g.mean(), "Median": g.median(), "Std_Dev": g.std(), "Min": g.min(), "Max": g.max(),
        "Pass_Rate_%": long.groupby("Subject")["Passed"].mean() * 100,
        "Distinction_Rate_%": long.groupby("Subject")["Distinction"].mean() * 100,
    }).round(1).reset_index()

    known = long[long["Gender"].isin(["Male", "Female"])]
    by_gender = known.pivot_table(index="Subject", columns="Gender", values="Score", aggfunc="mean").round(1)
    if {"Male", "Female"} <= set(by_gender.columns):
        by_gender["Gap_F_minus_M"] = (by_gender["Female"] - by_gender["Male"]).round(1)
    by_gender = by_gender.reset_index()

    grade_bins = pd.cut(long["Score"], [0, C.PASS_MARK, 55, 70, C.DISTINCTION_MARK, 100.01], right=False,
                        labels=[f"Fail (<{C.PASS_MARK})", f"{C.PASS_MARK}-54", "55-69", f"70-{C.DISTINCTION_MARK - 1}",
                                f"Distinction ({C.DISTINCTION_MARK}+)"])
    distribution = pd.crosstab(long["Subject"], grade_bins).reset_index()
    distribution.columns.name = None

    corr = df[C.SUBJECTS + ["Study_Hours", "Attendance_Percentage"]].corr().round(2)
    corr.index = corr.columns = [c.replace("_Score", "").replace("_Percentage", "") for c in corr.columns]

    focus = (df["Best_Subject"].value_counts().rename("Best_For_Students").to_frame()
             .join(df["Weakest_Subject"].value_counts().rename("Weakest_For_Students")).fillna(0).astype(int)
             .reset_index().rename(columns={"index": "Subject", "Best_Subject": "Subject"}))
    return {"summary": summary, "by_gender": by_gender, "distribution": distribution,
            "correlation": corr, "focus": focus, "long": long}
