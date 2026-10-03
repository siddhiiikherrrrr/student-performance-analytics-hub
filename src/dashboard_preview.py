"""Render a pixel-faithful preview of the Power BI 'Executive Overview' page from real data."""
from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from . import charts as ch
from . import config as C

T = C.THEME


def render(df, kpis: dict, insights, top_overall, path: Path) -> None:
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=T["bg"])
    bg = fig.add_axes([0, 0, 1, 1])
    bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")

    def card(x, y, w, h):
        bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.006",
                                    fc=T["card"], ec=T["border"], lw=1))

    def inner(x, y, w, h, title, fn, donut=False):
        card(x, y, w, h)
        ax = fig.add_axes([x + 0.035 * (16 / 16) * w, y + 0.16 * h, w * 0.9, h * 0.62])
        ch.style_ax(ax)
        if donut:
            ax.grid(False)
            for s in ax.spines.values():
                s.set_visible(False)
        fn(ax, df)
        bg.text(x + 0.012, y + h - 0.03, title, color=T["text"], fontsize=10.5, fontweight="bold", va="center")

    # header ---------------------------------------------------------------
    bg.add_patch(Rectangle((0, 0.925), 1, 0.075, fc="#070D1F", ec="none"))
    bg.add_patch(Rectangle((0.03, 0.945), 0.006, 0.035, fc=T["cyan"], ec="none"))
    bg.text(0.045, 0.973, "Student Performance Analytics Hub", color=T["text"], fontsize=17, fontweight="bold", va="center")
    bg.text(0.045, 0.944, "Executive Overview  |  Academic cohort analysis", color=T["muted"], fontsize=9, va="center")
    for i, lbl in enumerate(["Overview", "Attendance", "Subjects", "Top Performers", "Risk Monitor"]):
        x = 0.53 + i * 0.09
        active = i == 0
        bg.text(x, 0.96, lbl, color=T["cyan"] if active else T["muted"], fontsize=9, fontweight="bold" if active else "normal")
        if active:
            bg.add_patch(Rectangle((x, 0.936), 0.05, 0.003, fc=T["cyan"], ec="none"))

    # filter chips -----------------------------------------------------------
    for i, lbl in enumerate(["Gender: All", "Attendance Band: All", "Risk Level: All", "Subject: All", "Grade: All"]):
        x = 0.03 + i * 0.145
        bg.add_patch(FancyBboxPatch((x, 0.868), 0.135, 0.036, boxstyle="round,pad=0,rounding_size=0.008",
                                    fc=T["card"], ec=T["border"], lw=1))
        bg.text(x + 0.01, 0.886, lbl, color=T["muted"], fontsize=8.5, va="center")
        bg.text(x + 0.125, 0.886, "v", color=T["cyan"], fontsize=8, va="center", ha="center")

    # KPI cards -------------------------------------------------------------
    items = [("TOTAL STUDENTS", kpis["Total Students"], "in analysis", T["cyan"]),
             ("AVG SCORE", kpis["Average Score"], "across 3 subjects", T["cyan"]),
             ("AVG ATTENDANCE", kpis["Average Attendance"], f"{kpis['Chronic Absentees']} chronic absentees", T["amber"]),
             ("PASS RATE", kpis["Pass Rate (all subjects)"], "pass every subject", T["green"]),
             ("AT-RISK STUDENTS", kpis["At-Risk Students (High+Medium)"], f"{kpis['High-Risk Students']} high risk", T["red"]),
             ("TOP PERFORMERS", kpis["Top Performers (Top 10%)"], "top 10% by average", T["green"])]
    w = (0.94 - 5 * 0.01) / 6
    for i, (lbl, val, sub, col) in enumerate(items):
        x = 0.03 + i * (w + 0.01)
        card(x, 0.74, w, 0.11)
        bg.add_patch(Rectangle((x, 0.74 + 0.11 - 0.006), w, 0.006, fc=col, ec="none"))
        bg.text(x + 0.012, 0.815, lbl, color=T["muted"], fontsize=8, fontweight="bold")
        bg.text(x + 0.012, 0.774, str(val), color=T["text"], fontsize=22, fontweight="bold")
        bg.text(x + 0.012, 0.751, sub, color=col, fontsize=8)

    # row 2 -----------------------------------------------------------------
    y2, h2 = 0.37, 0.345
    card(0.03, y2, 0.27, h2)
    bg.text(0.042, y2 + h2 - 0.03, "Executive Summary", color=T["text"], fontsize=10.5, fontweight="bold", va="center")
    bg.add_patch(Rectangle((0.042, y2 + h2 - 0.048), 0.03, 0.003, fc=T["cyan"], ec="none"))
    picks = insights[insights.Category.isin(["Overview", "Attendance", "Risk", "Subjects"])].drop_duplicates("Category")
    yy = y2 + h2 - 0.078
    for r in picks.itertuples():
        col = {"Critical": T["red"], "Warning": T["amber"], "Positive": T["green"]}.get(r.Severity, T["cyan"])
        bg.add_patch(Rectangle((0.042, yy - 0.05), 0.003, 0.052, fc=col, ec="none"))
        bg.text(0.05, yy, r.Category.upper(), color=col, fontsize=7.5, fontweight="bold", va="top")
        bg.text(0.05, yy - 0.014, textwrap.fill(r.Insight, 58), color=T["text"], fontsize=7.2, va="top", linespacing=1.3)
        yy -= 0.061
    inner(0.31, y2, 0.39, h2, "Attendance vs Performance", ch.draw_scatter)
    inner(0.71, y2, 0.26, h2, "Risk Distribution", ch.draw_risk_donut, donut=True)

    # row 3 -----------------------------------------------------------------
    y3, h3 = 0.03, 0.325
    inner(0.03, y3, 0.27, h3, "Average Score by Subject", ch.draw_subject_bars)
    inner(0.31, y3, 0.27, h3, "Score by Attendance Band", ch.draw_band_bars)
    card(0.59, y3, 0.38, h3)
    bg.text(0.602, y3 + h3 - 0.03, "Top 5 Performers", color=T["text"], fontsize=10.5, fontweight="bold", va="center")
    heads = [("#", 0.602), ("Student", 0.63), ("Avg", 0.80), ("Attend.", 0.86), ("Study h", 0.92)]
    for lbl, x in heads:
        bg.text(x, y3 + h3 - 0.075, lbl, color=T["muted"], fontsize=8, fontweight="bold")
    for i, r in enumerate(top_overall.head(5).itertuples()):
        yy = y3 + h3 - 0.112 - i * 0.043
        if i % 2 == 0:
            bg.add_patch(Rectangle((0.598, yy - 0.016), 0.364, 0.035, fc=T["bg"], ec="none", alpha=0.5))
        bg.text(0.602, yy, str(r.Score_Rank), color=T["cyan"], fontsize=9, fontweight="bold", va="center")
        bg.text(0.63, yy, r.Student_Name, color=T["text"], fontsize=9, va="center")
        bg.text(0.80, yy, f"{r.Avg_Score:.1f}", color=T["cyan"], fontsize=9, fontweight="bold", va="center")
        bg.text(0.86, yy, f"{r.Attendance_Percentage:.0f}%", color=T["text"], fontsize=9, va="center")
        bg.text(0.92, yy, f"{r.Study_Hours:.1f}", color=T["text"], fontsize=9, va="center")

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120, facecolor=T["bg"])
    plt.close(fig)
