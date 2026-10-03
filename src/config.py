"""Central configuration: paths, business thresholds, and the visual theme."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "student_performance_raw.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"
FIG_DIR = REPORTS_DIR / "figures"

SUBJECTS = ["Math_Score", "Science_Score", "English_Score"]

# ---- Business rules (tune these; everything downstream adapts) -------------
PASS_MARK = 40                # minimum score to pass a subject
DISTINCTION_MARK = 85         # score considered a distinction
ATTENDANCE_THRESHOLD = 75     # below this = chronic absenteeism
MAX_STUDY_HOURS = 16          # anything above is treated as invalid

ATTENDANCE_BINS = [0, 60, 75, 85, 95, 100.01]
ATTENDANCE_LABELS = ["<60%", "60-75%", "75-85%", "85-95%", "95-100%"]
STUDY_BINS = [0, 2, 4, 6, MAX_STUDY_HOURS + 0.01]
STUDY_LABELS = ["<2h", "2-4h", "4-6h", "6h+"]
GRADE_BINS = [-float("inf"), 40, 55, 70, 85, float("inf")]
GRADE_LABELS = ["F", "D", "C", "B", "A"]

# ---- Risk model: points per signal, summed to a 0-100 score -----------------
RISK_HIGH_CUTOFF = 60
RISK_MEDIUM_CUTOFF = 30

# ---- Visual theme (shared by charts, dashboard preview, Power BI theme) -----
THEME = {
    "bg": "#0A1128", "card": "#111C3A", "border": "#1E2D52",
    "cyan": "#22D3EE", "sky": "#38BDF8", "blue": "#3B82F6",
    "green": "#34D399", "amber": "#FBBF24", "red": "#F87171",
    "text": "#E2E8F0", "muted": "#94A3B8",
}
