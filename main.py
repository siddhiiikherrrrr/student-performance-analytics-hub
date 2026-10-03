"""Student Performance Analytics Hub - pipeline entry point.

    python main.py                      # uses data/raw/student_performance_raw.xlsx
    python main.py --input my_file.xlsx
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from src import (attendance_analysis, charts, config as C, dashboard_preview, data_cleaning,
                 exporter, features, insights, report_builder, risk_detection, subject_analysis,
                 top_performers)

log = logging.getLogger("hub")


def build_kpis(df: pd.DataFrame, att: dict, risk: dict) -> dict:
    return {
        "Total Students": f"{len(df):,}",
        "Average Score": f"{df['Avg_Score'].mean():.1f}",
        "Average Attendance": f"{att['summary']['avg_attendance']:.1f}%",
        "Average Study Hours": f"{df['Study_Hours'].mean():.1f}",
        "Pass Rate (all subjects)": f"{df['All_Subjects_Passed'].mean() * 100:.1f}%",
        "Chronic Absentees": att["summary"]["chronic_absentees"],
        "At-Risk Students (High+Medium)": risk["high"] + risk["medium"],
        "High-Risk Students": risk["high"],
        "Top Performers (Top 10%)": int((df["Performance_Tier"] == "Top 10%").sum()),
    }


def run(input_path: Path = C.RAW_FILE) -> dict:
    log.info("Loading %s", input_path)
    raw = pd.read_excel(input_path, sheet_name="Students")

    clean_df, qa = data_cleaning.clean(raw)
    log.info("Cleaned: %d -> %d rows (%d duplicates, %d imputed)", qa["rows_in"], qa["rows_out"],
             qa["duplicates_removed"], qa["rows_imputed"])

    students = risk_detection.assess(features.enrich(clean_df))
    att = attendance_analysis.analyze(students)
    subj = subject_analysis.analyze(students)
    top = top_performers.analyze(students)
    risk = risk_detection.analyze(students)
    kpis = build_kpis(students, att, risk)
    ins = insights.generate(students, qa)

    # exports ------------------------------------------------------------------
    kpi_df = pd.DataFrame({"KPI": kpis.keys(), "Value": [str(v) for v in kpis.values()]})
    qa_df = pd.DataFrame({"Check": [k for k, v in qa.items() if not isinstance(v, dict)],
                          "Value": [v for v in qa.values() if not isinstance(v, dict)]})
    exporter.write_excel({
        "Executive_Summary": kpi_df, "Students": students, "Attendance_Bands": att["bands"],
        "Subject_Summary": subj["summary"], "Top_Performers": top["top_overall"],
        "Risk_Watchlist": risk["watchlist"], "Insights": ins, "Data_Quality": qa_df,
    }, C.PROCESSED_DIR / "student_analytics_output.xlsx")
    exporter.write_csvs({
        "students_clean": students, "subject_scores_long": subj["long"], "attendance_bands": att["bands"],
        "risk_watchlist": risk["watchlist"], "top_performers": top["top_overall"],
        "top_by_subject": top["top_by_subject"], "kpi_summary": kpi_df, "insights": ins,
    }, C.PROCESSED_DIR)

    # visuals + report ---------------------------------------------------------------
    charts.save_all(students, C.FIG_DIR)
    dashboard_preview.render(students, kpis, ins, top["top_overall"], C.REPORTS_DIR / "dashboard_preview.png")
    report_builder.build(students, qa, kpis, att, subj, top, risk, ins, C.REPORTS_DIR / "analysis_report.md")
    log.info("Done. Outputs in %s and %s", C.PROCESSED_DIR, C.REPORTS_DIR)
    return {"students": students, "qa": qa, "kpis": kpis, "insights": ins, "att": att,
            "subj": subj, "top": top, "risk": risk}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=C.RAW_FILE)
    res = run(ap.parse_args().input)
    print("\nKPIs")
    for k, v in res["kpis"].items():
        print(f"  {k:<34}{v}")
    print("\nInsights")
    for r in res["insights"].itertuples():
        print(f"  [{r.Severity:<8}] {r.Category}: {r.Insight}")
