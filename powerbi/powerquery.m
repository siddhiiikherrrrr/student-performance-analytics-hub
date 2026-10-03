// Power Query (M) - paste into Home > Transform data > New Source > Blank Query > Advanced Editor.
// Set the parameter below to the absolute path of the repo's data/processed folder.
// Create ONE query per block; name them exactly: students, subject_scores, attendance_bands, insights.

// ---------------- Parameter ----------------
let DataFolder = "C:\Projects\student-performance-analytics-hub\data\processed\" in DataFolder

// ---------------- students (fact table, 1 row per student) ----------------
let
    Source  = Csv.Document(File.Contents(DataFolder & "students_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed   = Table.TransformColumnTypes(Headers, {
        {"Attendance_Percentage", type number}, {"Study_Hours", type number},
        {"Math_Score", type number}, {"Science_Score", type number}, {"English_Score", type number},
        {"Avg_Score", type number}, {"Total_Score", type number}, {"Risk_Score", Int64.Type},
        {"Attendance_Band_Order", Int64.Type}, {"Risk_Level_Order", Int64.Type},
        {"Score_Rank", Int64.Type}, {"Percentile", type number}, {"Failing_Subjects", Int64.Type},
        {"All_Subjects_Passed", type logical}, {"Was_Imputed", type logical}})
in
    Typed

// ---------------- subject_scores (1 row per student-subject) ----------------
let
    Source  = Csv.Document(File.Contents(DataFolder & "subject_scores_long.csv"), [Delimiter=",", Encoding=65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed   = Table.TransformColumnTypes(Headers, {{"Score", type number}, {"Passed", type logical}, {"Distinction", type logical}})
in
    Typed

// ---------------- attendance_bands ----------------
let
    Source  = Csv.Document(File.Contents(DataFolder & "attendance_bands.csv"), [Delimiter=",", Encoding=65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Headers

// ---------------- insights (feeds the Executive Summary text card) ----------------
let
    Source  = Csv.Document(File.Contents(DataFolder & "insights.csv"), [Delimiter=",", Encoding=65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Headers

// ---------------- Alternative: load the Excel output instead of CSVs ----------------
// let Source = Excel.Workbook(File.Contents(DataFolder & "student_analytics_output.xlsx"), true),
//     Students = Source{[Item="Students", Kind="Sheet"]}[Data]
// in Students
