"""
Shared Pytest Fixtures for Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Step 13 - Test Cases Framework
"""

import os
import sqlite3
import pytest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'app.db')

@pytest.fixture(scope="session")
def db_connection():
    """Provides a SQLite connection to data/app.db with foreign keys enabled."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def tiny_dataset():
    """
    A controlled 10-row dataset with known deterministic outcomes for formula validation.
    Total: 10 employees, 2 in Sales (both left), 1 in Sales (stayed) => Sales Attrition = 66.67%
    OverTime = Yes: 4 employees (4 left = 100%), OverTime = No: 6 employees (0 left = 0%)
    Early tenure (<2 yr): 4 employees (4 left = 100%)
    """
    return pd.DataFrame({
        'EmployeeID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Department': ['Sales', 'Sales', 'Sales', 'R&D', 'R&D', 'R&D', 'R&D', 'HR', 'HR', 'HR'],
        'JobRole': [
            'Sales Representative', 'Sales Executive', 'Sales Executive',
            'Laboratory Technician', 'Research Scientist', 'Research Scientist', 'Research Director',
            'HR Executive', 'HR Executive', 'HR Manager'
        ],
        'OverTime': ['Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No'],
        'MonthlyIncome': [21000, 24500, 46000, 22000, 72000, 84000, 145000, 32000, 48000, 115000],
        'YearsAtCompany': [1, 1, 3, 1, 6, 8, 12, 1, 4, 15],
        'PercentSalaryHike': [12, 13, 18, 11, 19, 21, 24, 12, 17, 22],
        'JobSatisfaction': [1, 1, 3, 2, 4, 4, 4, 1, 3, 4],
        'EnvironmentSatisfaction': [1, 2, 3, 1, 4, 3, 4, 2, 3, 4],
        'WorkLifeBalance': [1, 1, 3, 1, 4, 3, 4, 1, 3, 4],
        'Age': [24, 27, 36, 25, 42, 45, 52, 28, 38, 49],
        'Attrition': ['Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No']
    })
