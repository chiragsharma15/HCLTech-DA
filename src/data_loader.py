"""
Data Loading, Caching & Validation Pipeline
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-02
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'app.db')

def validate_schema(df: pd.DataFrame) -> bool:
    """
    Validates physical schema constraints V-01 to V-08.
    Raises ValueError with detailed diagnostic if any check fails.
    """
    if len(df) < 1000:
        raise ValueError(f"Schema Validation V-01 Failed: Expected >= 1000 rows, got {len(df)}")
    
    if df.shape[1] < 30:
        raise ValueError(f"Schema Validation V-02 Failed: Expected >= 30 columns in view, got {df.shape[1]}")
        
    key_cols = ['EmployeeID', 'Age', 'DepartmentName', 'JobRoleName', 'MonthlyIncome', 'Attrition']
    missing_keys = [c for c in key_cols if c not in df.columns]
    if missing_keys:
        raise ValueError(f"Schema Validation V-03 Failed: Missing required columns {missing_keys}")
        
    null_counts = df[key_cols].isnull().sum()
    if null_counts.sum() > 0:
        raise ValueError(f"Schema Validation V-04 Failed: Found nulls in key columns: {null_counts.to_dict()}")
        
    if not df['Attrition'].isin(['Yes', 'No']).all():
        raise ValueError("Schema Validation V-05 Failed: Non-binary values in Attrition column")
        
    if not df['Age'].between(18, 65).all():
        raise ValueError("Schema Validation V-06 Failed: Employee Age out of bounds (18 to 65)")
        
    if not (df['MonthlyIncome'] > 0).all():
        raise ValueError("Schema Validation V-07 Failed: Non-positive MonthlyIncome detected")
        
    if not df['EmployeeID'].is_unique:
        raise ValueError("Schema Validation V-08 Failed: Duplicate EmployeeIDs detected in active view")
        
    return True


@st.cache_data(ttl=3600, show_spinner="Loading workforce analytics data from SQLite...")
def load_data() -> pd.DataFrame:
    """
    Loads analytical view from SQLite database with in-memory caching.
    Ensures foreign keys are enabled and validates schema on return.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found at {DB_PATH}. Please run src/generate_data.py first.")
        
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    query = "SELECT * FROM v_employee_analysis"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Run validation
    validate_schema(df)
    
    # Type optimizations
    df['EmployeeID'] = df['EmployeeID'].astype(int)
    df['Age'] = df['Age'].astype(int)
    df['MonthlyIncome'] = df['MonthlyIncome'].astype(int)
    df['PercentSalaryHike'] = df['PercentSalaryHike'].astype(int)
    df['DistanceFromHome'] = df['DistanceFromHome'].astype(int)
    df['YearsAtCompany'] = df['YearsAtCompany'].astype(int)
    
    return df


def clean_raw_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstration data cleaning pipeline handling the injected raw anomalies:
    1. Imputes missing NumCompaniesWorked with median (2.0)
    2. Imputes missing DistanceFromHome with role/dept median
    3. Deduplicates on EmployeeID keeping first entry
    4. Caps extreme distance outliers at 30 km
    5. Corrects negative/extreme salary outliers
    """
    df = df_raw.copy()
    
    # 1. Deduplication
    df = df.drop_duplicates(subset=['EmployeeID'], keep='first')
    
    # 2. Impute missing NumCompaniesWorked
    median_comp = df['NumCompaniesWorked'].median()
    df['NumCompaniesWorked'] = df['NumCompaniesWorked'].fillna(median_comp)
    
    # 3. Impute missing DistanceFromHome
    median_dist = df['DistanceFromHome'].median()
    df['DistanceFromHome'] = df['DistanceFromHome'].fillna(median_dist)
    
    # 4. Cap distance outliers (> 30 km)
    df['DistanceFromHome'] = np.clip(df['DistanceFromHome'], 1, 30)
    
    # 5. Correct salary outliers (negative or 10x typos)
    df['MonthlyIncome'] = df['MonthlyIncome'].apply(lambda x: abs(x) if x < 0 else (x // 10 if x > 2000000 else x))
    
    return df
