"""
Statistical and KPI Analysis Computation Tests (pytest)
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Step 13 - Technical Tests (TC-T-09 to TC-T-14)
"""

import pytest
import pandas as pd
import numpy as np
from scipy import stats

def calculate_attrition_rate(df: pd.DataFrame) -> float:
    """Helper implementing BRL-01 formula: (Departures / Total Headcount) * 100."""
    if len(df) == 0:
        return 0.0
    return float((df['Attrition'] == 'Yes').mean() * 100)

def classify_salary_band(income: float) -> str:
    """Helper implementing BRL-04 salary band tiers."""
    if income <= 25000:
        return 'Entry'
    elif income <= 50000:
        return 'Mid-Junior'
    elif income <= 100000:
        return 'Senior'
    else:
        return 'Leadership'

def classify_tenure_band(years: float) -> str:
    """Helper implementing BRL-02 tenure band classifications."""
    if years < 2:
        return 'Early-Tenure (<2 yr)'
    elif years <= 5:
        return 'Mid-Tenure (2-5 yr)'
    elif years <= 10:
        return 'Senior-Tenure (6-10 yr)'
    else:
        return 'Veteran (10+ yr)'


def test_kpi_overall_attrition_rate_formula(tiny_dataset):
    """TC-T-09: Verify overall attrition rate formula on controlled 10-row dataset."""
    # In tiny_dataset: 4 leavers out of 10 employees => exactly 40.0%
    rate = calculate_attrition_rate(tiny_dataset)
    assert rate == pytest.approx(40.0, 0.01)

def test_kpi_department_attrition_rate(tiny_dataset):
    """TC-T-10: Verify department-wise grouping and attrition rates on known data."""
    dept_rates = tiny_dataset.groupby('Department').apply(calculate_attrition_rate)
    
    # Sales: 2 left out of 3 = 66.67%
    assert dept_rates['Sales'] == pytest.approx(66.67, 0.1)
    # R&D: 1 left out of 4 = 25.00%
    assert dept_rates['R&D'] == pytest.approx(25.0, 0.1)
    # HR: 1 left out of 3 = 33.33%
    assert dept_rates['HR'] == pytest.approx(33.33, 0.1)

def test_kpi_overtime_attrition_rate(tiny_dataset):
    """TC-T-11: Verify OverTime=Yes vs OverTime=No cohort attrition computation."""
    ot_rate = calculate_attrition_rate(tiny_dataset[tiny_dataset['OverTime'] == 'Yes'])
    no_ot_rate = calculate_attrition_rate(tiny_dataset[tiny_dataset['OverTime'] == 'No'])
    
    # In tiny_dataset: 4 Yes (4 left = 100.0%), 6 No (0 left = 0.0%)
    assert ot_rate == pytest.approx(100.0, 0.01)
    assert no_ot_rate == pytest.approx(0.0, 0.01)

def test_salary_band_binning_logic():
    """TC-T-12: Verify compensation band assignment rules."""
    assert classify_salary_band(18000) == 'Entry'
    assert classify_salary_band(25000) == 'Entry'
    assert classify_salary_band(25001) == 'Mid-Junior'
    assert classify_salary_band(50000) == 'Mid-Junior'
    assert classify_salary_band(75000) == 'Senior'
    assert classify_salary_band(100000) == 'Senior'
    assert classify_salary_band(100001) == 'Leadership'
    assert classify_salary_band(185000) == 'Leadership'

def test_tenure_band_binning_logic():
    """TC-T-13: Verify tenure classification logic and early-tenure (<2 yr) flag."""
    assert classify_tenure_band(0) == 'Early-Tenure (<2 yr)'
    assert classify_tenure_band(1) == 'Early-Tenure (<2 yr)'
    assert classify_tenure_band(1.9) == 'Early-Tenure (<2 yr)'
    assert classify_tenure_band(2) == 'Mid-Tenure (2-5 yr)'
    assert classify_tenure_band(5) == 'Mid-Tenure (2-5 yr)'
    assert classify_tenure_band(6) == 'Senior-Tenure (6-10 yr)'
    assert classify_tenure_band(10) == 'Senior-Tenure (6-10 yr)'
    assert classify_tenure_band(11) == 'Veteran (10+ yr)'

def test_chi_square_contingency_calculation(tiny_dataset):
    """TC-T-14: Verify chi-square test on 2x2 contingency table (Overtime vs Attrition)."""
    contingency = pd.crosstab(tiny_dataset['OverTime'], tiny_dataset['Attrition'])
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
    
    assert dof == 1, "Degrees of freedom for 2x2 table must be 1"
    assert p_val < 0.05, f"Expected statistically significant difference, got p = {p_val}"

def test_spearman_rank_correlation(tiny_dataset):
    """TC-T-15: Verify Spearman rank correlation between Likert satisfaction and departure."""
    # Convert Attrition to binary indicator: Yes=1, No=0
    attr_binary = (tiny_dataset['Attrition'] == 'Yes').astype(int)
    corr, p_val = stats.spearmanr(tiny_dataset['JobSatisfaction'], attr_binary)
    
    # Dissatisfied employees left => negative correlation expected
    assert corr < 0, f"Expected negative correlation between satisfaction and attrition, got {corr}"

def test_salary_hike_median_comparison(tiny_dataset):
    """TC-T-16: Verify median salary hike calculation between retained and departed employees."""
    leavers_hike = tiny_dataset[tiny_dataset['Attrition'] == 'Yes']['PercentSalaryHike'].median()
    stayers_hike = tiny_dataset[tiny_dataset['Attrition'] == 'No']['PercentSalaryHike'].median()
    
    assert leavers_hike < stayers_hike, f"Expected leavers median ({leavers_hike}) < stayers median ({stayers_hike})"
