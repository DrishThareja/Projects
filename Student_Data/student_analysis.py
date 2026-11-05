"""
Student Performance Analysis
Cleans the Kaggle "Students Performance in Exams" dataset with Pandas,
loads it into SQLite and answers questions with SQL queries.

Run:  python student_analysis.py
Needs StudentsPerformance.csv in the same folder.
"""

import sqlite3
import pandas as pd

# 1. Load the data
df = pd.read_csv("StudentsPerformance.csv")
print("Rows and columns (raw):", df.shape)

# 2. Clean column names: "math score" -> "math_score", "race/ethnicity" -> "race_ethnicity"
df.columns = [c.strip().lower().replace(" ", "_").replace("/", "_") for c in df.columns]

# 3. Check data quality
print("\nMissing values per column:")
print(df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# 4. Create a new column: average of the three subject scores
df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1).round(2)
print("Rows after cleaning:", len(df))

# 5. Load into SQLite
conn = sqlite3.connect("students.db")
df.to_sql("students", conn, if_exists="replace", index=False)

# 6. SQL queries
queries = {
    "1. Average score by test preparation course": """
        SELECT test_preparation_course,
               COUNT(*) AS students,
               ROUND(AVG(average_score), 2) AS avg_score
        FROM students
        GROUP BY test_preparation_course;""",

    "2. Average score by parental education": """
        SELECT parental_level_of_education,
               COUNT(*) AS students,
               ROUND(AVG(average_score), 2) AS avg_score
        FROM students
        GROUP BY parental_level_of_education
        ORDER BY avg_score DESC;""",

    "3. Average score by lunch type": """
        SELECT lunch,
               ROUND(AVG(average_score), 2) AS avg_score
        FROM students
        GROUP BY lunch;""",

    "4. Average score by gender": """
        SELECT gender,
               ROUND(AVG(math_score), 2) AS avg_math,
               ROUND(AVG(reading_score), 2) AS avg_reading,
               ROUND(AVG(writing_score), 2) AS avg_writing
        FROM students
        GROUP BY gender;""",

    "5. Top 10 students": """
        SELECT gender, parental_level_of_education, test_preparation_course, average_score
        FROM students
        ORDER BY average_score DESC
        LIMIT 10;""",

    "6. Students with math score below 40": """
        SELECT COUNT(*) AS low_math_students
        FROM students
        WHERE math_score < 40;""",

    "7. Students scoring above the overall average": """
        SELECT COUNT(*) AS above_average
        FROM students
        WHERE average_score > (SELECT AVG(average_score) FROM students);""",
}

for title, sql in queries.items():
    print("\n" + title)
    print(pd.read_sql(sql, conn).to_string(index=False))

conn.close()
