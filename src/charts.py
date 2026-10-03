"""Chart primitives in the navy/cyan theme (reused by the dashboard preview)."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import config as C

T = C.THEME
RISK_COLORS = {"High": T["red"], "Medium": T["amber"], "Low": T["cyan"]}


def style_ax(ax, title=None):
    ax.set_facecolor("none")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(T["border"])
    ax.tick_params(colors=T["muted"], labelsize=8)
    ax.xaxis.label.set_color(T["muted"])
    ax.yaxis.label.set_color(T["muted"])
    ax.grid(axis="y", color=T["border"], alpha=0.6, lw=0.6)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, color=T["text"], fontsize=11, fontweight="bold", loc="left", pad=10)


def draw_scatter(ax, df):
    ax.scatter(df["Attendance_Percentage"], df["Avg_Score"], c=df["Risk_Level"].map(RISK_COLORS),
               s=14, alpha=0.8, edgecolor="none")
    m, b = np.polyfit(df["Attendance_Percentage"], df["Avg_Score"], 1)
    xs = np.linspace(df["Attendance_Percentage"].min(), 100, 50)
    ax.plot(xs, m * xs + b, color=T["text"], lw=1.3, ls="--")
    ax.set_xlabel("Attendance %", fontsize=8)
    ax.set_ylabel("Average score", fontsize=8)
    for lvl, col in RISK_COLORS.items():
        ax.scatter([], [], c=col, s=18, label=lvl)
    leg = ax.legend(frameon=False, fontsize=7, loc="lower right", ncol=3, labelcolor=T["muted"])


def draw_subject_bars(ax, df):
    means = df[C.SUBJECTS].mean()
    labels = [s.replace("_Score", "") for s in means.index]
    bars = ax.bar(labels, means.values, color=[T["cyan"], T["sky"], T["blue"]], width=0.55)
    ax.set_ylim(0, 100)
    pr = (df[C.SUBJECTS] >= C.PASS_MARK).mean() * 100
    for b, v, p in zip(bars, means.values, pr.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}", ha="center", color=T["text"], fontsize=9,
                fontweight="bold")
        ax.text(b.get_x() + b.get_width() / 2, 6, f"{p:.0f}% pass", ha="center", color=T["bg"], fontsize=7.5)
    ax.set_ylabel("Mean score", fontsize=8)


def draw_risk_donut(ax, df):
    order = ["Low", "Medium", "High"]
    counts = df["Risk_Level"].value_counts().reindex(order).fillna(0)
    ax.pie(counts, colors=[RISK_COLORS[k] for k in order], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.36, edgecolor=T["card"], linewidth=2))
    at_risk = (counts["High"] + counts["Medium"]) / counts.sum() * 100
    ax.text(0, 0.06, f"{at_risk:.0f}%", ha="center", va="center", color=T["text"], fontsize=20, fontweight="bold")
    ax.text(0, -0.2, "at risk", ha="center", va="center", color=T["muted"], fontsize=8)
    ax.legend([f"{k}  {int(counts[k])}" for k in order], loc="center left", bbox_to_anchor=(0.92, 0.5),
              frameon=False, fontsize=8, labelcolor=T["text"])
    ax.set_aspect("equal")


def draw_band_bars(ax, df):
    g = (df.groupby(["Attendance_Band_Order", "Attendance_Band"])
         .agg(n=("Student_ID", "count"), s=("Avg_Score", "mean")).reset_index().sort_values("Attendance_Band_Order"))
    bars = ax.bar(g["Attendance_Band"], g["s"], color=T["cyan"], width=0.6)
    ax.set_ylim(0, 100)
    for b, s, n in zip(bars, g["s"], g["n"]):
        ax.text(b.get_x() + b.get_width() / 2, s + 2, f"{s:.0f}", ha="center", color=T["text"], fontsize=9, fontweight="bold")
        ax.text(b.get_x() + b.get_width() / 2, 5, f"n={n}", ha="center", color=T["bg"], fontsize=7.5)
    ax.set_xlabel("Attendance band", fontsize=8)
    ax.set_ylabel("Avg score", fontsize=8)


def draw_distribution(ax, df):
    ax.hist(df["Avg_Score"], bins=20, color=T["cyan"], edgecolor=T["bg"], alpha=0.9)
    ax.axvline(C.PASS_MARK, color=T["red"], ls="--", lw=1.2)
    ax.text(C.PASS_MARK + 1, ax.get_ylim()[1] * 0.92, "pass mark", color=T["red"], fontsize=8)
    ax.set_xlabel("Average score", fontsize=8)
    ax.set_ylabel("Students", fontsize=8)


CHARTS = {
    "attendance_vs_score": ("Attendance vs Performance", draw_scatter, (7, 4.2)),
    "subject_performance": ("Average Score by Subject", draw_subject_bars, (6, 4.2)),
    "risk_distribution": ("Risk Distribution", draw_risk_donut, (6, 4.2)),
    "attendance_bands": ("Score by Attendance Band", draw_band_bars, (6.5, 4.2)),
    "score_distribution": ("Distribution of Average Scores", draw_distribution, (6.5, 4.2)),
}


def save_all(df, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for key, (title, fn, size) in CHARTS.items():
        fig, ax = plt.subplots(figsize=size, facecolor=T["bg"])
        style_ax(ax, title)
        if fn is draw_risk_donut:
            ax.grid(False)
            for s in ax.spines.values():
                s.set_visible(False)
        fn(ax, df)
        fig.tight_layout()
        p = out_dir / f"{key}.png"
        fig.savefig(p, dpi=150, facecolor=T["bg"])
        plt.close(fig)
        paths[key] = p
    return paths
