"""
Dataset Generation Script for Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Step: 10 - Dataset Generation
Target: data/app.db, data/employee_attrition_data.xlsx, data/*.csv
"""

import os
import random
import sqlite3
import datetime
import numpy as np
import pandas as pd
from faker import Faker
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Set fixed random seeds for strict reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
fake = Faker('en_IN')
Faker.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, 'app.db')
EXCEL_PATH = os.path.join(DATA_DIR, 'employee_attrition_data.xlsx')

NUM_EMPLOYEES = 1250  # Planned fact rows (satisfies 150+ and 1000+ requirements)

print("=" * 70)
print(f"STARTING DATASET GENERATION (N = {NUM_EMPLOYEES}, Seed = {RANDOM_SEED})")
print("=" * 70)

# ──────────────────────────────────────────────────────────────
# 1. GENERATE MASTER / DIMENSION TABLES
# ──────────────────────────────────────────────────────────────

# 1.1 departments
departments_data = [
    {"DepartmentID": 1, "DepartmentName": "Human Resources"},
    {"DepartmentID": 2, "DepartmentName": "Research & Development"},
    {"DepartmentID": 3, "DepartmentName": "Sales"},
    {"DepartmentID": 4, "DepartmentName": "Engineering"},
    {"DepartmentID": 5, "DepartmentName": "Marketing"},
    {"DepartmentID": 6, "DepartmentName": "Finance"},
]
df_departments = pd.DataFrame(departments_data)

# 1.2 job_roles
job_roles_data = [
    {"JobRoleID": 1, "JobRoleName": "Research Scientist", "DepartmentID": 2},
    {"JobRoleID": 2, "JobRoleName": "Laboratory Technician", "DepartmentID": 2},
    {"JobRoleID": 3, "JobRoleName": "Research Director", "DepartmentID": 2},
    {"JobRoleID": 4, "JobRoleName": "Sales Executive", "DepartmentID": 3},
    {"JobRoleID": 5, "JobRoleName": "Sales Representative", "DepartmentID": 3},
    {"JobRoleID": 6, "JobRoleName": "Software Engineer", "DepartmentID": 4},
    {"JobRoleID": 7, "JobRoleName": "Senior Developer", "DepartmentID": 4},
    {"JobRoleID": 8, "JobRoleName": "QA Engineer", "DepartmentID": 4},
    {"JobRoleID": 9, "JobRoleName": "HR Executive", "DepartmentID": 1},
    {"JobRoleID": 10, "JobRoleName": "HR Manager", "DepartmentID": 1},
    {"JobRoleID": 11, "JobRoleName": "Marketing Specialist", "DepartmentID": 5},
    {"JobRoleID": 12, "JobRoleName": "Financial Analyst", "DepartmentID": 6},
]
df_job_roles = pd.DataFrame(job_roles_data)

# 1.3 education_levels
education_levels_data = [
    {"EducationLevelID": 1, "EducationLevelName": "Below College", "EducationRank": 1},
    {"EducationLevelID": 2, "EducationLevelName": "College", "EducationRank": 2},
    {"EducationLevelID": 3, "EducationLevelName": "Bachelor", "EducationRank": 3},
    {"EducationLevelID": 4, "EducationLevelName": "Master", "EducationRank": 4},
    {"EducationLevelID": 5, "EducationLevelName": "Doctor", "EducationRank": 5},
]
df_education_levels = pd.DataFrame(education_levels_data)

print(f"[1/5] Master tables generated: {len(df_departments)} departments, {len(df_job_roles)} roles, {len(df_education_levels)} education levels.")

# ──────────────────────────────────────────────────────────────
# 2. GENERATE EMPLOYEES FACT TABLE & SATISFACTION SURVEYS
# ──────────────────────────────────────────────────────────────

education_fields = ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other']
ed_field_weights = [0.35, 0.25, 0.15, 0.15, 0.05, 0.05]

# Department distribution weights
dept_ids = [1, 2, 3, 4, 5, 6]
dept_weights = [0.08, 0.38, 0.26, 0.16, 0.06, 0.06]

# Map department to allowed roles
dept_to_roles = {
    1: [9, 10],       # HR Exec, HR Mgr
    2: [1, 2, 3],     # Research Scientist, Lab Tech, Research Director
    3: [4, 5],        # Sales Exec, Sales Rep
    4: [6, 7, 8],     # Software Eng, Senior Dev, QA Eng
    5: [11],          # Marketing Specialist
    6: [12]           # Financial Analyst
}

role_job_levels = {
    1: [2, 3],        # Research Scientist: L2, L3
    2: [1, 2],        # Lab Tech: L1, L2
    3: [4, 5],        # Research Director: L4, L5
    4: [2, 3],        # Sales Executive: L2, L3
    5: [1, 2],        # Sales Rep: L1, L2
    6: [2, 3],        # Software Engineer: L2, L3
    7: [3, 4],        # Senior Dev: L3, L4
    8: [1, 2],        # QA Engineer: L1, L2
    9: [1, 2],        # HR Executive: L1, L2
    10: [4, 5],       # HR Manager: L4, L5
    11: [2, 3],       # Marketing Specialist: L2, L3
    12: [2, 3]        # Financial Analyst: L2, L3
}

employees_list = []
surveys_list = []

start_date_sim = datetime.date(2020, 1, 1)
end_date_sim = datetime.date(2025, 12, 31)
date_range_days = (end_date_sim - start_date_sim).days

for i in range(NUM_EMPLOYEES):
    emp_id = 1000 + i + 1
    
    # Demographics
    age = int(np.clip(np.random.normal(36, 8.5), 18, 65))
    gender = np.random.choice(['Male', 'Female'], p=[0.60, 0.40])
    marital = np.random.choice(['Single', 'Married', 'Divorced'], p=[0.32, 0.50, 0.18])
    ed_level_id = int(np.random.choice([1, 2, 3, 4, 5], p=[0.10, 0.18, 0.42, 0.24, 0.06]))
    ed_field = np.random.choice(education_fields, p=ed_field_weights)
    
    # Department & Role
    dept_id = int(np.random.choice(dept_ids, p=dept_weights))
    possible_roles = dept_to_roles[dept_id]
    role_id = int(np.random.choice(possible_roles))
    
    possible_levels = role_job_levels[role_id]
    job_level = int(np.random.choice(possible_levels))
    
    # Experience and Tenure
    max_total_work = max(0, age - 20)
    total_working_years = int(np.clip(np.random.beta(2, 3) * max_total_work, 0, 40))
    
    max_company_years = min(total_working_years, age - 21) if age > 21 else 0
    years_at_company = int(np.clip(np.random.beta(1.5, 3) * max_company_years, 0, 40)) if max_company_years > 0 else 0
    
    years_in_curr_role = int(np.random.randint(0, min(years_at_company, 18) + 1)) if years_at_company > 0 else 0
    years_since_promo = int(np.random.randint(0, min(years_at_company, 15) + 1)) if years_at_company > 0 else 0
    years_with_manager = int(np.random.randint(0, min(years_at_company, 17) + 1)) if years_at_company > 0 else 0
    
    num_companies = int(np.clip(np.random.poisson(2), 0, 9))
    training_times = int(np.clip(np.random.poisson(2.8), 0, 6))
    
    # Commute distance (1 to 30 km)
    distance_from_home = int(np.clip(np.random.exponential(8) + 1, 1, 30))
    
    # Overtime probability (about 28% of employees)
    overtime_prob = 0.32 if role_id in [2, 5, 8] else (0.30 if dept_id == 4 else 0.24)
    overtime = 'Yes' if np.random.rand() < overtime_prob else 'No'
    
    # Base compensation scaled by job level (INR 15,000 to 180,000)
    level_base_salary = {
        1: (18000, 32000),
        2: (32000, 58000),
        3: (58000, 95000),
        4: (95000, 140000),
        5: (140000, 195000)
    }
    low_sal, high_sal = level_base_salary[job_level]
    monthly_income = int(np.random.uniform(low_sal, high_sal) + (years_at_company * 800))
    # Round to nearest 100
    monthly_income = int(round(monthly_income, -2))
    
    # Salary band assignment
    if monthly_income <= 25000:
        salary_band = 'Entry'
    elif monthly_income <= 50000:
        salary_band = 'Mid-Junior'
    elif monthly_income <= 100000:
        salary_band = 'Senior'
    else:
        salary_band = 'Leadership'
        
    percent_salary_hike = int(np.random.randint(11, 26))
    stock_option = int(np.random.choice([0, 1, 2, 3], p=[0.40, 0.35, 0.15, 0.10]))
    
    # ── INJECTED CORRELATION LOGIC FOR ATTRITION ──
    # Baseline departure risk score
    attrition_score = 0.0
    
    # Pattern 1: Overtime Burnout (High impact)
    if overtime == 'Yes':
        attrition_score += 0.32
    else:
        attrition_score -= 0.12
        
    # Pattern 2: Early Tenure (< 2 years)
    if years_at_company < 2:
        attrition_score += 0.28
    elif years_at_company >= 7:
        attrition_score -= 0.20
        
    # Pattern 3: Salary Band & Compensation Inequity
    if salary_band == 'Entry':
        attrition_score += 0.25
    elif salary_band == 'Mid-Junior':
        attrition_score += 0.10
    elif salary_band == 'Leadership':
        attrition_score -= 0.30
        
    # Pattern 4: Salary Hike percentage
    if percent_salary_hike <= 13:
        attrition_score += 0.18
    elif percent_salary_hike >= 20:
        attrition_score -= 0.15
        
    # Pattern 5: Department & Role Stress
    if role_id in [2, 5]: # Lab Tech or Sales Rep
        attrition_score += 0.18
    elif role_id in [3, 10]: # Research Director or HR Manager
        attrition_score -= 0.25
        
    # Pattern 6: Long commute + Single
    if distance_from_home > 20:
        attrition_score += 0.12
    if marital == 'Single':
        attrition_score += 0.10
        
    # Generate Satisfaction Survey Ratings (influenced by overtime and salary)
    job_sat_probs = [0.15, 0.25, 0.35, 0.25]
    env_sat_probs = [0.15, 0.25, 0.35, 0.25]
    wlb_probs = [0.12, 0.28, 0.40, 0.20]
    
    if overtime == 'Yes':
        wlb_probs = [0.38, 0.36, 0.18, 0.08] # Much poorer work-life balance
        job_sat_probs = [0.28, 0.34, 0.26, 0.12]
        
    if salary_band == 'Entry':
        job_sat_probs = [0.30, 0.35, 0.25, 0.10]
        
    job_satisfaction = int(np.random.choice([1, 2, 3, 4], p=job_sat_probs))
    env_satisfaction = int(np.random.choice([1, 2, 3, 4], p=env_sat_probs))
    wlb = int(np.random.choice([1, 2, 3, 4], p=wlb_probs))
    rel_satisfaction = int(np.random.choice([1, 2, 3, 4], p=[0.12, 0.28, 0.40, 0.20]))
    perf_rating = int(np.random.choice([1, 2, 3, 4], p=[0.05, 0.20, 0.60, 0.15]))
    job_involvement = int(np.random.choice([1, 2, 3, 4], p=[0.10, 0.30, 0.45, 0.15]))
    
    # Dissatisfaction multiplier on attrition
    if job_satisfaction == 1:
        attrition_score += 0.28
    elif job_satisfaction == 4:
        attrition_score -= 0.20
        
    if env_satisfaction == 1:
        attrition_score += 0.18
        
    if wlb == 1:
        attrition_score += 0.22
    elif wlb == 4:
        attrition_score -= 0.15
        
    # Convert attrition score to probability using sigmoid function
    # Calibrated to yield overall attrition rate between 18% and 22% (NovaTech baseline)
    prob_leaving = 1.0 / (1.0 + np.exp(-(attrition_score - 1.52)))
    attrition = 'Yes' if np.random.rand() < prob_leaving else 'No'
    
    # Dates
    # Random joining date over past 5 years
    join_offset = random.randint(0, date_range_days)
    date_joining = start_date_sim + datetime.timedelta(days=join_offset)
    
    date_leaving = None
    if attrition == 'Yes':
        # Departure occurs between 60 days after joining and current date (or end of 2026)
        tenure_days = max(60, int(years_at_company * 365.25) + random.randint(-90, 90))
        date_leaving_calc = date_joining + datetime.timedelta(days=tenure_days)
        max_possible_leave = datetime.date(2026, 10, 31)
        if date_leaving_calc > max_possible_leave:
            date_leaving_calc = max_possible_leave - datetime.timedelta(days=random.randint(1, 90))
        if date_leaving_calc <= date_joining:
            date_leaving_calc = date_joining + datetime.timedelta(days=random.randint(60, 180))
        date_leaving = date_leaving_calc.strftime('%Y-%m-%d')
        
    employees_list.append({
        "EmployeeID": emp_id,
        "Age": age,
        "Gender": gender,
        "MaritalStatus": marital,
        "EducationField": ed_field,
        "EducationLevelID": ed_level_id,
        "DepartmentID": dept_id,
        "JobRoleID": role_id,
        "JobLevel": job_level,
        "MonthlyIncome": monthly_income,
        "PercentSalaryHike": percent_salary_hike,
        "StockOptionLevel": stock_option,
        "DistanceFromHome": distance_from_home,
        "OverTime": overtime,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_in_curr_role,
        "YearsSinceLastPromotion": years_since_promo,
        "YearsWithCurrManager": years_with_manager,
        "TotalWorkingYears": total_working_years,
        "NumCompaniesWorked": num_companies,
        "TrainingTimesLastYear": training_times,
        "DateOfJoining": date_joining.strftime('%Y-%m-%d'),
        "DateOfLeaving": date_leaving,
        "Attrition": attrition,
        "SalaryBand": salary_band
    })
    
    surveys_list.append({
        "SurveyID": i + 1,
        "EmployeeID": emp_id,
        "JobSatisfaction": job_satisfaction,
        "EnvironmentSatisfaction": env_satisfaction,
        "WorkLifeBalance": wlb,
        "RelationshipSatisfaction": rel_satisfaction,
        "PerformanceRating": perf_rating,
        "JobInvolvement": job_involvement
    })

df_employees = pd.DataFrame(employees_list)
df_surveys = pd.DataFrame(surveys_list)

overall_attrition_rate = (df_employees['Attrition'] == 'Yes').mean() * 100
ot_attrition = (df_employees[df_employees['OverTime'] == 'Yes']['Attrition'] == 'Yes').mean() * 100
no_ot_attrition = (df_employees[df_employees['OverTime'] == 'No']['Attrition'] == 'Yes').mean() * 100
early_tenure_attrition = (df_employees[df_employees['YearsAtCompany'] < 2]['Attrition'] == 'Yes').mean() * 100

print(f"[2/5] Generated {len(df_employees)} employees and {len(df_surveys)} survey records.")
print(f"      - Overall Attrition Rate: {overall_attrition_rate:.2f}% (Target: 17-20%)")
print(f"      - Overtime Attrition Rate: {ot_attrition:.2f}% vs No-Overtime: {no_ot_attrition:.2f}%")
print(f"      - Early-Tenure (<2 yrs) Attrition Rate: {early_tenure_attrition:.2f}%")

# ──────────────────────────────────────────────────────────────
# 3. GENERATE RAW DIRTY DATASET (WITH INJECTED QUALITY ISSUES)
# ──────────────────────────────────────────────────────────────
# Creating df_employees_raw with:
# 1. ~2.5% Missing values in NumCompaniesWorked (31 rows)
# 2. ~2.0% Missing values in DistanceFromHome (25 rows)
# 3. 3 Duplicate employee rows
# 4. 3 Outliers (extreme distance, extreme income typo)

df_employees_raw = df_employees.copy()

# 1. Missing values injection
missing_indices_numcomp = np.random.choice(df_employees_raw.index, size=31, replace=False)
df_employees_raw.loc[missing_indices_numcomp, 'NumCompaniesWorked'] = np.nan

missing_indices_dist = np.random.choice(df_employees_raw.index, size=25, replace=False)
df_employees_raw.loc[missing_indices_dist, 'DistanceFromHome'] = np.nan

# 2. Duplicate records (3 duplicated rows appended)
dup_rows = df_employees_raw.iloc[[14, 185, 412]].copy()
df_employees_raw = pd.concat([df_employees_raw, dup_rows], ignore_index=True)

# 3. Outlier values
outlier_idx_1 = 45  # Distance outlier
df_employees_raw.loc[outlier_idx_1, 'DistanceFromHome'] = 98  # Typo (allowed: 1-30)

outlier_idx_2 = 120 # Negative income outlier
df_employees_raw.loc[outlier_idx_2, 'MonthlyIncome'] = -15000 # Erroneous entry

outlier_idx_3 = 280 # Extreme salary typo
df_employees_raw.loc[outlier_idx_3, 'MonthlyIncome'] = 4500000 # Extra zero

print(f"[3/5] Injected Data Quality Issues into raw extract:")
print(f"      - Missing NumCompaniesWorked: {df_employees_raw['NumCompaniesWorked'].isna().sum()} rows")
print(f"      - Missing DistanceFromHome: {df_employees_raw['DistanceFromHome'].isna().sum()} rows")
print(f"      - Injected Duplicates: {len(dup_rows)} duplicate records")
print(f"      - Injected Outliers: Distance=98 km, Negative Salary=-15000, 10x Salary=4500000")

# ──────────────────────────────────────────────────────────────
# 4. POPULATE SQLITE DATABASE (data/app.db)
# ──────────────────────────────────────────────────────────────
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# DDL Statements
ddl_script = """
CREATE TABLE departments (
    DepartmentID    INTEGER PRIMARY KEY AUTOINCREMENT,
    DepartmentName  TEXT    NOT NULL UNIQUE
);

CREATE TABLE job_roles (
    JobRoleID       INTEGER PRIMARY KEY AUTOINCREMENT,
    JobRoleName     TEXT    NOT NULL UNIQUE,
    DepartmentID    INTEGER NOT NULL,
    FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE education_levels (
    EducationLevelID   INTEGER PRIMARY KEY AUTOINCREMENT,
    EducationLevelName TEXT    NOT NULL UNIQUE,
    EducationRank      INTEGER NOT NULL CHECK (EducationRank BETWEEN 1 AND 5)
);

CREATE TABLE employees (
    EmployeeID          INTEGER PRIMARY KEY,
    Age                 INTEGER NOT NULL CHECK (Age BETWEEN 18 AND 65),
    Gender              TEXT    NOT NULL CHECK (Gender IN ('Male', 'Female')),
    MaritalStatus       TEXT    NOT NULL CHECK (MaritalStatus IN ('Single', 'Married', 'Divorced')),
    EducationField      TEXT    NOT NULL,
    EducationLevelID    INTEGER NOT NULL,
    DepartmentID        INTEGER NOT NULL,
    JobRoleID           INTEGER NOT NULL,
    JobLevel            INTEGER NOT NULL CHECK (JobLevel BETWEEN 1 AND 5),
    MonthlyIncome       INTEGER NOT NULL CHECK (MonthlyIncome > 0),
    PercentSalaryHike   INTEGER NOT NULL CHECK (PercentSalaryHike BETWEEN 11 AND 25),
    StockOptionLevel    INTEGER NOT NULL CHECK (StockOptionLevel BETWEEN 0 AND 3),
    DistanceFromHome    INTEGER NOT NULL CHECK (DistanceFromHome BETWEEN 1 AND 30),
    OverTime            TEXT    NOT NULL CHECK (OverTime IN ('Yes', 'No')),
    YearsAtCompany      INTEGER NOT NULL CHECK (YearsAtCompany >= 0),
    YearsInCurrentRole  INTEGER NOT NULL CHECK (YearsInCurrentRole >= 0),
    YearsSinceLastPromotion INTEGER NOT NULL CHECK (YearsSinceLastPromotion >= 0),
    YearsWithCurrManager INTEGER NOT NULL CHECK (YearsWithCurrManager >= 0),
    TotalWorkingYears   INTEGER NOT NULL CHECK (TotalWorkingYears >= 0),
    NumCompaniesWorked  INTEGER NOT NULL CHECK (NumCompaniesWorked >= 0),
    TrainingTimesLastYear INTEGER NOT NULL CHECK (TrainingTimesLastYear BETWEEN 0 AND 6),
    DateOfJoining       TEXT    NOT NULL,
    DateOfLeaving       TEXT,
    Attrition           TEXT    NOT NULL CHECK (Attrition IN ('Yes', 'No')),
    SalaryBand          TEXT    NOT NULL CHECK (SalaryBand IN ('Entry', 'Mid-Junior', 'Senior', 'Leadership')),
    FOREIGN KEY (EducationLevelID) REFERENCES education_levels(EducationLevelID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (DepartmentID)     REFERENCES departments(DepartmentID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (JobRoleID)        REFERENCES job_roles(JobRoleID)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE satisfaction_surveys (
    SurveyID                INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeID              INTEGER NOT NULL UNIQUE,
    JobSatisfaction         INTEGER NOT NULL CHECK (JobSatisfaction BETWEEN 1 AND 4),
    EnvironmentSatisfaction INTEGER NOT NULL CHECK (EnvironmentSatisfaction BETWEEN 1 AND 4),
    WorkLifeBalance         INTEGER NOT NULL CHECK (WorkLifeBalance BETWEEN 1 AND 4),
    RelationshipSatisfaction INTEGER NOT NULL CHECK (RelationshipSatisfaction BETWEEN 1 AND 4),
    PerformanceRating       INTEGER NOT NULL CHECK (PerformanceRating BETWEEN 1 AND 4),
    JobInvolvement          INTEGER NOT NULL CHECK (JobInvolvement BETWEEN 1 AND 4),
    FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_emp_dept ON employees(DepartmentID);
CREATE INDEX idx_emp_role ON employees(JobRoleID);
CREATE INDEX idx_emp_attrition ON employees(Attrition);
CREATE INDEX idx_emp_overtime ON employees(OverTime);
CREATE INDEX idx_emp_leaving ON employees(DateOfLeaving);
CREATE INDEX idx_survey_emp ON satisfaction_surveys(EmployeeID);

CREATE VIEW v_employee_analysis AS
SELECT 
    e.EmployeeID, e.Age, e.Gender, e.MaritalStatus,
    e.EducationField, el.EducationLevelName, el.EducationRank,
    d.DepartmentName,
    jr.JobRoleName, e.JobLevel,
    e.MonthlyIncome, e.SalaryBand, e.PercentSalaryHike, e.StockOptionLevel,
    e.DistanceFromHome, e.OverTime,
    e.YearsAtCompany, e.YearsInCurrentRole, e.YearsSinceLastPromotion,
    e.YearsWithCurrManager, e.TotalWorkingYears, e.NumCompaniesWorked,
    e.TrainingTimesLastYear,
    e.DateOfJoining, e.DateOfLeaving, e.Attrition,
    s.JobSatisfaction, s.EnvironmentSatisfaction,
    s.WorkLifeBalance, s.RelationshipSatisfaction,
    s.PerformanceRating, s.JobInvolvement,
    CASE WHEN e.Age < 30 THEN 'Under 30'
         WHEN e.Age BETWEEN 30 AND 40 THEN '30-40'
         WHEN e.Age BETWEEN 41 AND 50 THEN '41-50'
         ELSE 'Over 50' END AS AgeBracket,
    CASE WHEN e.YearsAtCompany < 2 THEN 'Early-Tenure (<2 yr)'
         WHEN e.YearsAtCompany BETWEEN 2 AND 5 THEN 'Mid-Tenure (2-5 yr)'
         WHEN e.YearsAtCompany BETWEEN 6 AND 10 THEN 'Senior-Tenure (6-10 yr)'
         ELSE 'Veteran (10+ yr)' END AS TenureBand
FROM employees e
LEFT JOIN departments d ON e.DepartmentID = d.DepartmentID
LEFT JOIN job_roles jr ON e.JobRoleID = jr.JobRoleID
LEFT JOIN education_levels el ON e.EducationLevelID = el.EducationLevelID
LEFT JOIN satisfaction_surveys s ON e.EmployeeID = s.EmployeeID;
"""

cursor.executescript(ddl_script)
conn.commit()

# Insert Master Data
df_departments.to_sql('departments', conn, if_exists='append', index=False)
df_job_roles.to_sql('job_roles', conn, if_exists='append', index=False)
df_education_levels.to_sql('education_levels', conn, if_exists='append', index=False)

# Insert Clean Fact Data (app.db receives validated data)
df_employees.to_sql('employees', conn, if_exists='append', index=False)
df_surveys.to_sql('satisfaction_surveys', conn, if_exists='append', index=False)
conn.commit()

# Verify View
df_view_check = pd.read_sql("SELECT * FROM v_employee_analysis LIMIT 5", conn)
print(f"[4/5] Populated SQLite database at {DB_PATH}")
print(f"      - View 'v_employee_analysis' active with {df_view_check.shape[1]} columns")
conn.close()

# ──────────────────────────────────────────────────────────────
# 5. EXPORT CSVs AND MASTER EXCEL WORKBOOK
# ──────────────────────────────────────────────────────────────

# 5.1 Export Individual CSVs
df_departments.to_csv(os.path.join(DATA_DIR, 'departments.csv'), index=False)
df_job_roles.to_csv(os.path.join(DATA_DIR, 'job_roles.csv'), index=False)
df_education_levels.to_csv(os.path.join(DATA_DIR, 'education_levels.csv'), index=False)
df_employees.to_csv(os.path.join(DATA_DIR, 'employees.csv'), index=False)
df_surveys.to_csv(os.path.join(DATA_DIR, 'satisfaction_surveys.csv'), index=False)
df_employees_raw.to_csv(os.path.join(DATA_DIR, 'employees_raw.csv'), index=False)

# 5.2 Build Master Excel Workbook with openpyxl
print("[5/5] Building styled Master Excel Workbook...")

# Extract full view data for Excel inclusion
conn = sqlite3.connect(DB_PATH)
df_full_view = pd.read_sql("SELECT * FROM v_employee_analysis", conn)
conn.close()

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default sheet

# Styling rules
font_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_cell = Font(name="Calibri", size=9.5, color="000000")
fill_hdr = PatternFill(start_color="1B3A5C", end_color="1B3A5C", fill_type="solid")
fill_zebra = PatternFill(start_color="F7F9FA", end_color="F7F9FA", fill_type="solid")
fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
thin_border = Border(left=Side(style='thin', color='CCCCCC'),
                     right=Side(style='thin', color='CCCCCC'),
                     top=Side(style='thin', color='CCCCCC'),
                     bottom=Side(style='thin', color='CCCCCC'))

sheets_to_add = [
    ("departments", df_departments),
    ("job_roles", df_job_roles),
    ("education_levels", df_education_levels),
    ("employees", df_employees),
    ("satisfaction_surveys", df_surveys),
    ("v_employee_analysis", df_full_view),
    ("raw_employees_with_issues", df_employees_raw),
]

for sheet_name, df_data in sheets_to_add:
    ws = wb.create_sheet(title=sheet_name)
    ws.views.sheetView[0].showGridLines = True
    
    # Write headers
    headers = list(df_data.columns)
    ws.append(headers)
    ws.row_dimensions[1].height = 24
    
    for c_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c_idx)
        cell.font = font_hdr
        cell.fill = fill_hdr
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    # Write data rows
    for r_idx, row_values in enumerate(df_data.values, 2):
        ws.append([None if pd.isna(v) else v for v in row_values])
        ws.row_dimensions[r_idx].height = 19
        row_fill = fill_zebra if r_idx % 2 == 0 else fill_white
        
        for c_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.font = font_cell
            cell.fill = row_fill
            cell.border = thin_border
            if isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
    # Auto-adjust column widths
    for col_idx, col_name in enumerate(headers, 1):
        max_len = max(len(str(col_name)), 10)
        # sample first 30 rows
        for r in range(2, min(len(df_data) + 2, 32)):
            val = ws.cell(row=r, column=col_idx).value
            if val is not None:
                max_len = max(max_len, min(len(str(val)), 35))
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = max_len + 3
        
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(df_data)+1}"
    ws.freeze_panes = "A2"

wb.save(EXCEL_PATH)
print(f"      - Excel Workbook saved to: {EXCEL_PATH}")

print("=" * 70)
print("DATASET GENERATION AND EXPORT COMPLETED SUCCESSFULLY!")
print("=" * 70)
