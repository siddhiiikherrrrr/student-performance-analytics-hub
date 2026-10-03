"""Run with:  pytest -q   (or  python tests/test_pipeline.py  if pytest is unavailable)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import config as C
from src import data_cleaning, features, risk_detection


def _dirty():
    return pd.DataFrame({
        "Student_ID": ["s1", "S1", "S2", "S3", "S4"],
        "Student_Name": ["  ann  lee", "ANN LEE", "bob ray", "cy poe", "dee fox"],
        "Gender": ["f", "F", "MALE ", "x", "Female"],
        "Attendance_Percentage": [90, 90, 150, "80%", np.nan],
        "Study_Hours": [4, 4, 3, -1, 5],
        "Math_Score": [70, 70, 60, 55, 105],
        "Science_Score": [70, 70, 60, 55, 65],
        "English_Score": [70, 70, 60, 55, 65],
    })


def test_cleaning_rules():
    df, qa = data_cleaning.clean(_dirty())
    assert len(df) == 4 and qa["duplicates_removed"] == 1                     # S1 duplicate dropped
    assert df.loc[df.Student_ID == "S1", "Student_Name"].iloc[0] == "Ann Lee"
    assert set(df.Gender) <= {"Male", "Female", "Unknown"}
    assert df.Attendance_Percentage.between(0, 100).all()                      # 150 removed, "80%" parsed
    assert df.Study_Hours.between(0, C.MAX_STUDY_HOURS).all() and df.Math_Score.max() <= 100
    assert df.isna().sum().sum() == 0 and qa["rows_imputed"] >= 3


def _scored(att, hrs, m, s, e):
    d = pd.DataFrame({"Student_ID": ["X"], "Student_Name": ["X"], "Gender": ["Male"],
                      "Attendance_Percentage": [att], "Study_Hours": [hrs],
                      "Math_Score": [m], "Science_Score": [s], "English_Score": [e]})
    return risk_detection.assess(features.enrich(d)).iloc[0]


def test_risk_levels():
    assert _scored(50, 1, 30, 35, 38).Risk_Level == "High"
    assert _scored(98, 6, 90, 88, 92).Risk_Level == "Low"
    assert _scored(70, 2.5, 52, 50, 58).Risk_Level in {"Medium", "High"}


def test_features_and_bounds():
    r = _scored(80, 4, 90, 60, 30)
    assert r.Best_Subject == "Math" and r.Weakest_Subject == "English"
    assert r.Failing_Subjects == 1 and not r.All_Subjects_Passed
    assert 0 <= r.Risk_Score <= 100


def test_end_to_end():
    import main
    out = main.run()
    s = out["students"]
    assert s.Student_ID.is_unique and len(s) == out["qa"]["rows_out"]
    assert s.Risk_Level.isin(["High", "Medium", "Low"]).all()
    assert (C.PROCESSED_DIR / "student_analytics_output.xlsx").exists()
    assert len(out["insights"]) >= 10


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("PASS", name)
