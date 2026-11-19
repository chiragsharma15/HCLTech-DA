"""
Data Layer and Database Integrity Tests (pytest)
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Step 13 - Technical Tests (TC-T-01 to TC-T-06)
"""

import os
import sqlite3
import pytest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'app.db')

def test_database_file_exists():
    """TC-T-01: Verify SQLite database file exists and is populated."""
    assert os.path.exists(DB_PATH), "SQLite database data/app.db does not exist!"
    assert os.path.getsize(DB_PATH) > 50000, f"Database file is too small ({os.path.getsize(DB_PATH)} bytes)"

def test_sqlite_foreign_keys_enabled(db_connection):
    """TC-T-02: Verify foreign key enforcement is active in SQLite connection."""
    fk_status = db_connection.execute("PRAGMA foreign_keys;").fetchone()[0]
    assert fk_status == 1, "PRAGMA foreign_keys is not enabled!"

def test_table_presence_and_row_counts(db_connection):
    """TC-T-03: Verify all 5 physical tables exist with expected minimum row counts."""
    cursor = db_connection.cursor()
    expected_tables = {
        'departments': 6,
        'job_roles': 12,
        'education_levels': 5,
        'employees': 1000,       # At least 1,000 (currently 1,250)
        'satisfaction_surveys': 1000
    }
    for table, min_rows in expected_tables.items():
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert count >= min_rows, f"Table {table} has {count} rows, expected >= {min_rows}"

def test_primary_key_uniqueness(db_connection):
    """TC-T-04: Verify Primary Keys in employees and surveys are 100% unique."""
    cursor = db_connection.cursor()
    # Check employees
    emp_dup = cursor.execute("""
        SELECT EmployeeID, COUNT(*) FROM employees GROUP BY EmployeeID HAVING COUNT(*) > 1
    """).fetchall()
    assert len(emp_dup) == 0, f"Duplicate EmployeeIDs detected in employees: {emp_dup}"
    
    # Check surveys
    surv_dup = cursor.execute("""
        SELECT SurveyID, COUNT(*) FROM satisfaction_surveys GROUP BY SurveyID HAVING COUNT(*) > 1
    """).fetchall()
    assert len(surv_dup) == 0, f"Duplicate SurveyIDs detected in satisfaction_surveys: {surv_dup}"

def test_foreign_key_integrity(db_connection):
    """TC-T-05: Run PRAGMA foreign_key_check to ensure zero referential integrity violations."""
    cursor = db_connection.cursor()
    violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    assert len(violations) == 0, f"Foreign key integrity violations detected: {violations}"

def test_view_structure_and_column_counts(db_connection):
    """TC-T-06: Verify analytical view v_employee_analysis exists with >= 30 columns."""
    cursor = db_connection.cursor()
    cursor.execute("PRAGMA table_info(v_employee_analysis);")
    cols = [r[1] for r in cursor.fetchall()]
    assert len(cols) >= 30, f"v_employee_analysis has only {len(cols)} columns, expected >= 30"
    
    # Verify key binned attributes exist in view
    assert 'AgeBracket' in cols, "AgeBracket column missing from v_employee_analysis"
    assert 'TenureBand' in cols, "TenureBand column missing from v_employee_analysis"
    assert 'DepartmentName' in cols, "DepartmentName column missing from v_employee_analysis"

def test_domain_range_constraints(db_connection):
    """TC-T-07: Verify numerical intervals (Age 18-65, Income > 0, Distance 1-30, Likert 1-4)."""
    df_emp = pd.read_sql("SELECT Age, MonthlyIncome, DistanceFromHome, PercentSalaryHike, JobLevel FROM employees", db_connection)
    
    assert df_emp['Age'].between(18, 65).all(), "Invalid Age detected (outside 18-65)"
    assert (df_emp['MonthlyIncome'] > 0).all(), "Negative or zero MonthlyIncome detected"
    assert df_emp['DistanceFromHome'].between(1, 30).all(), "DistanceFromHome outside 1-30 km"
    assert df_emp['PercentSalaryHike'].between(11, 25).all(), "PercentSalaryHike outside 11-25%"
    assert df_emp['JobLevel'].isin([1, 2, 3, 4, 5]).all(), "Invalid JobLevel detected"

def test_raw_data_quality_anomalies_present():
    """TC-T-08: Verify raw test CSV contains injected anomalies for cleaning exercises."""
    raw_csv = os.path.join(DATA_DIR, 'employees_raw.csv')
    assert os.path.exists(raw_csv), "Raw test CSV employees_raw.csv is missing!"
    df_raw = pd.read_csv(raw_csv)
    
    # Check missing values
    assert df_raw['NumCompaniesWorked'].isna().sum() > 0, "Missing values in NumCompaniesWorked not present"
    assert df_raw['DistanceFromHome'].isna().sum() > 0, "Missing values in DistanceFromHome not present"
    
    # Check duplicates
    assert df_raw.duplicated(subset=['EmployeeID']).sum() > 0, "Duplicate records in raw data not present"
    
    # Check outliers
    assert (df_raw['DistanceFromHome'] > 30).sum() > 0, "Distance outliers not present in raw data"
    assert ((df_raw['MonthlyIncome'] < 0) | (df_raw['MonthlyIncome'] > 250000)).sum() > 0, "Salary outliers not present in raw data"
