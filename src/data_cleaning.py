"""Module 1 - Data Cleaning.

Turns a messy Excel export into an analysis-ready table and returns an audit
report describing exactly what was changed (so nothing is silently altered).

Steps: schema validation -> text normalisation -> numeric coercion ->
de-duplication -> range validation -> median imputation -> rounding.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from . import config as C

REQUIRED = ["Student_ID", "Student_Name", "Gender", "Attendance_Percentage",
            "Study_Hours", "Math_Score", "Science_Score", "English_Score"]
NUMERIC = REQUIRED[3:]
GENDER_MAP = {"m": "Male", "male": "Male", "man": "Male", "boy": "Male",
              "f": "Female", "female": "Female", "woman": "Female", "girl": "Female"}
BOUNDS = {"Attendance_Percentage": (0, 100), "Study_Hours": (0, C.MAX_STUDY_HOURS),
          **{s: (0, 100) for s in C.SUBJECTS}}


def _standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"\s+", "_", str(c).strip()) for c in df.columns]
    canon = {c.lower(): c for c in REQUIRED}
    df.columns = [canon.get(c.lower(), c) for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Input file is missing required columns: {missing}")
    return df[REQUIRED]


def clean(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Return (clean_df, audit_report)."""
    report: dict = {"rows_in": int(len(raw))}
    df = _standardise_columns(raw)
    original = df[["Student_Name", "Gender"]].astype(str).copy()

    # 1. text normalisation ---------------------------------------------------
    for col in ["Student_ID", "Student_Name", "Gender"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
    df["Student_ID"] = df["Student_ID"].str.upper()
    df["Student_Name"] = (df["Student_Name"].str.replace(r"\s+", " ", regex=True)
                          .str.title().replace("", "Unknown"))
    df["Gender"] = df["Gender"].str.lower().map(GENDER_MAP).fillna("Unknown")
    report["names_standardised"] = int((original["Student_Name"] != df["Student_Name"]).sum())
    report["gender_labels_fixed"] = int((~original["Gender"].isin(["Male", "Female"])).sum())

    # 2. numeric coercion ("85%" -> 85.0, "n/a" -> NaN) ------------------------
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace("%", "", regex=False).str.strip(),
                                errors="coerce")

    # 3. drop rows with no ID, then de-duplicate on ID ---------------------------
    no_id = df["Student_ID"] == ""
    report["rows_missing_id_dropped"] = int(no_id.sum())
    df = df[~no_id]
    before = len(df)
    df = df.drop_duplicates(subset="Student_ID", keep="first")
    report["duplicates_removed"] = int(before - len(df))

    # 4. range validation: impossible values become missing -----------------------
    report["out_of_range_nullified"] = {}
    for col, (lo, hi) in BOUNDS.items():
        bad = df[col].notna() & ~df[col].between(lo, hi)
        report["out_of_range_nullified"][col] = int(bad.sum())
        df.loc[bad, col] = np.nan

    # 5. median imputation (robust to skew), with an audit flag ---------------------
    report["missing_before_imputation"] = {c: int(df[c].isna().sum()) for c in NUMERIC}
    df["Was_Imputed"] = df[NUMERIC].isna().any(axis=1)
    medians = df[NUMERIC].median()
    report["imputation_medians"] = {c: round(float(v), 2) for c, v in medians.items()}
    df[NUMERIC] = df[NUMERIC].fillna(medians)

    # 6. finish ------------------------------------------------------------------
    df[NUMERIC] = df[NUMERIC].round(1)
    df = df.sort_values("Student_ID").reset_index(drop=True)
    report["rows_out"] = int(len(df))
    report["rows_imputed"] = int(df["Was_Imputed"].sum())
    report["completeness_after_%"] = round(100 * (1 - df[REQUIRED].isna().mean().mean()), 2)
    return df, report
