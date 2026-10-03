# Output Data Dictionary (`students_clean.csv`)

| Column | Meaning |
|---|---|
| Total_Score / Avg_Score | Sum / mean of the three subject scores |
| Subject_Std | Spread across subjects (high = uneven profile) |
| Grade | A >= 85, B >= 70, C >= 55, D >= 40, F < 40 (by Avg_Score) |
| Attendance_Band / _Order | Band label and numeric sort key (for Power BI sort-by-column) |
| Study_Band | <2h, 2-4h, 4-6h, 6h+ |
| Best_Subject / Weakest_Subject | Highest / lowest scoring subject |
| Failing_Subjects / All_Subjects_Passed | Count of subjects below pass mark / boolean |
| Score_Rank / Percentile | Rank (1 = best, ties share rank) / percentile of Avg_Score |
| Performance_Tier | Top 10%, Upper Quartile, Mid Range, Lower Quartile |
| Study_Efficiency | Avg_Score per study hour |
| Risk_Score / Risk_Level / Risk_Level_Order | 0-100 score, High/Medium/Low, sort key |
| Primary_Risk_Driver / Risk_Factors / Recommended_Action | Explainability fields |
| Was_Imputed | True if any value was filled during cleaning |
