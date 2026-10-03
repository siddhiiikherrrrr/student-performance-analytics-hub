# Power BI Dashboard - Layout Specification

**Product name:** Student Performance Analytics Hub  
**Preview:** see [`reports/dashboard_preview.png`](../reports/dashboard_preview.png) (rendered from the real data)  
**Canvas:** 1280 x 720 (16:9) | **Theme:** `theme_navy_cyan.json` | **Font:** Segoe UI / Segoe UI Semibold

## 1. Design system

| Token | Hex | Use |
|---|---|---|
| Page background | `#0A1128` | Canvas |
| Header band | `#070D1F` | Top bar |
| Card surface | `#111C3A` | Every visual background |
| Card border | `#1E2D52` | 1px, 8px radius |
| Primary (cyan) | `#22D3EE` | KPIs, main series, active nav |
| Secondary | `#38BDF8` / `#3B82F6` | 2nd/3rd series |
| Success | `#34D399` | Pass rate, top performers |
| Warning | `#FBBF24` | Medium risk, attendance warnings |
| Danger | `#F87171` | High risk, failing |
| Text / Muted | `#E2E8F0` / `#94A3B8` | Titles, axis labels |

Rules: no gridline noise (light `#1E2D52` only), no chart borders inside cards, data labels on bars, titles left-aligned, 12-24px gutters, one accent colour per KPI card (top strip).

## 2. Global navigation and filters (all pages)

| Element | Position (x, y, w, h) | Notes |
|---|---|---|
| Header band + title | 0, 0, 1280, 56 | Rectangle + text: product name, page subtitle |
| Page navigator | 440, 12, 800, 32 | Button navigator, active = cyan underline |
| Slicer: Gender | 24, 68, 150, 32 | Dropdown |
| Slicer: Attendance_Band | 186, 68, 180, 32 | Dropdown, sort by `Attendance_Band_Order` |
| Slicer: Risk_Level | 378, 68, 150, 32 | Dropdown, sort by `Risk_Level_Order` |
| Slicer: Subject | 540, 68, 150, 32 | From `subject_scores[Subject]` |
| Slicer: Grade | 702, 68, 150, 32 | Dropdown |
| Reset button | 1160, 68, 96, 32 | Bookmark that clears slicers |

Sync all slicers across pages (View > Sync slicers). Add a **Drill-through** page (`Student Profile`) keyed on `Student_ID`.

## 3. Page 1 - Executive Overview

| Zone | Visual | Position (x, y, w, h) | Fields / measure |
|---|---|---|---|
| KPI row | 6 x Card (new) | y=112, h=88, w=194, gap 12; x = 24, 230, 436, 642, 848, 1054 | Total Students, Avg Score, Avg Attendance %, Pass Rate %, At-Risk Students, Top Performers |
| Left | Executive Summary (text card) | 24, 212, 344, 248 | `[Executive Summary]` measure + 3 rows from `insights` filtered by Category, coloured by Severity |
| Centre | Scatter | 380, 212, 500, 248 | X `Attendance_Percentage`, Y `Avg_Score`, legend `Risk_Level`, trend line on |
| Right | Donut | 892, 212, 364, 248 | Legend `Risk_Level`, values `Total Students`, centre label `[At-Risk %]` |
| Bottom-left | Clustered column | 24, 472, 344, 224 | Axis `subject_scores[Subject]`, values `[Subject Avg Score]`, data labels |
| Bottom-centre | Column | 380, 472, 344, 224 | Axis `Attendance_Band`, values `[Avg Score]` |
| Bottom-right | Table | 736, 472, 520, 224 | Top N (5) `Student_Name` by `Avg_Score`; add `Attendance_Percentage`, `Study_Hours`; data bars on Avg |

## 4. Page 2 - Attendance Analysis

- KPI strip: Avg Attendance %, Chronic Absentees, Attendance-Score Correlation, 95%+ attendance share.
- Column chart: student count by `Attendance_Band` (order column) with line = Avg Score.
- Scatter: attendance vs score, size = `Study_Hours`, colour = `Risk_Level`.
- Clustered bar: Avg Attendance by `Gender`.
- Table: chronic absentees (`Attendance_Percentage` < 75) with conditional-format background using `[Risk Colour]`.
- Insight callout: dynamic text "Every +10pp attendance is associated with +X marks" (from `insights`).

## 5. Page 3 - Subject Performance

- KPI strip: Subject Avg Score, Subject Pass Rate %, Distinction Rate %, Weakest Subject.
- Clustered column: average by `Subject` split by `Gender` (legend).
- 100% stacked bar: `Grade` distribution per `Subject`.
- Box/violin alternative: Histogram of `Score` bins (use `Score` binned by 10) by Subject small multiples.
- Matrix: `Subject` x `Attendance_Band` with Avg score heat-map (cyan gradient min `#1E3A5F` -> max `#22D3EE`).
- Slicer emphasis: Subject slicer switches to single-select on this page.

## 6. Page 4 - Top Performers

- KPI strip: Top Performers, Top-10% Avg Score, Avg Study Efficiency, Distinction Rate %.
- Table: rank 1-20 with data bars for each subject score.
- Bar: Top 5 per subject (small multiples by `Subject`, from `top_by_subject`).
- Scatter: `Study_Hours` vs `Avg_Score`, highlight `Performance_Tier` = "Top 10%".
- Card row: "Efficient learners" (upper quartile, below-median study time) count.

## 7. Page 5 - Risk Monitor

- KPI strip: At-Risk Students, High Risk Students, At-Risk %, top driver.
- Stacked bar: `Primary_Risk_Driver` by `Risk_Level`.
- Watchlist table (main visual, 60% of canvas): `Student_ID`, `Student_Name`, `Risk_Score` (data bars), `Risk_Level` (icon: red/amber dot), `Risk_Factors`, `Recommended_Action`. Sort by `Risk_Score` desc. Enable drill-through to `Student Profile`.
- Line/area: Risk share by `Attendance_Band`.
- Export: allow "Export data" on the table for teachers.

## 8. Drill-through page - Student Profile

Hidden page. Cards: name, grade, rank, percentile. Radar/column of three subject scores vs cohort average (`[Score Gap vs Cohort]`), attendance gauge (target 85%), `Risk_Factors` text, `Recommended_Action`.

## 9. Interactions and polish checklist

- [ ] Import `theme_navy_cyan.json` (View > Themes > Browse for themes)
- [ ] Page background `#0A1128`; hide page tabs, use navigator
- [ ] Tooltip page for scatter (name, attendance, avg, risk)
- [ ] Conditional formatting on KPI values using `[Attendance KPI Colour]` and `[Risk Colour]`
- [ ] Alt text on every visual; tab order top-to-bottom
- [ ] Set slicer default to "All"; add Reset bookmark
- [ ] Publish and schedule refresh once `data/processed` is on OneDrive/SharePoint
