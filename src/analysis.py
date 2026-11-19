"""
Statistical Computation and KPI Analytical Engine
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-03
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, Tuple

def calculate_attrition_rate(df: pd.DataFrame) -> float:
    """Computes attrition rate percentage: (Leavers / Total Headcount) * 100."""
    if len(df) == 0:
        return 0.0
    return float((df['Attrition'] == 'Yes').mean() * 100)


def compute_headline_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes top-level summary metrics for executive KPI cards."""
    total_count = len(df)
    if total_count == 0:
        return {
            "total_employees": "0",
            "total_leavers": "0",
            "attrition_rate": "0.00%",
            "avg_leaver_tenure": "0.0 yr",
            "raw_rate": 0.0
        }
        
    leavers_df = df[df['Attrition'] == 'Yes']
    total_leavers = len(leavers_df)
    rate = (total_leavers / total_count) * 100
    
    avg_tenure = leavers_df['YearsAtCompany'].mean() if total_leavers > 0 else 0.0
    
    return {
        "total_employees": f"{total_count:,}",
        "total_leavers": f"{total_leavers:,}",
        "attrition_rate": f"{rate:.2f}%",
        "avg_leaver_tenure": f"{avg_tenure:.1f} Years",
        "raw_rate": rate
    }


def get_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Computes monthly departure counts and cumulative attrition over time."""
    if len(df) == 0:
        return pd.DataFrame(columns=['YearMonth', 'LeaversCount', 'CumulativeLeavers'])
        
    leavers = df[df['Attrition'] == 'Yes'].copy()
    if leavers['DateOfLeaving'].isna().all() or len(leavers) == 0:
        return pd.DataFrame(columns=['YearMonth', 'LeaversCount', 'CumulativeLeavers'])
        
    leavers['YearMonth'] = leavers['DateOfLeaving'].str.slice(0, 7)
    trend = leavers.groupby('YearMonth').size().reset_index(name='LeaversCount')
    trend = trend.sort_values('YearMonth')
    trend['CumulativeLeavers'] = trend['LeaversCount'].cumsum()
    return trend


def get_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes headcount, departures, and turnover rate % per department, ranked descending."""
    if len(df) == 0:
        return pd.DataFrame(columns=['DepartmentName', 'TotalHeadcount', 'LeaverCount', 'AttritionRate', 'CriticalRole'])
        
    dept_group = df.groupby('DepartmentName').agg(
        TotalHeadcount=('EmployeeID', 'count'),
        LeaverCount=('Attrition', lambda x: (x == 'Yes').sum()),
        AttritionRate=('Attrition', lambda x: (x == 'Yes').mean() * 100)
    ).reset_index()
    
    # Identify highest turnover role in each department
    critical_roles = {}
    for dept in df['DepartmentName'].unique():
        dept_sub = df[df['DepartmentName'] == dept]
        role_rates = dept_sub.groupby('JobRoleName')['Attrition'].apply(lambda x: (x == 'Yes').mean() * 100)
        if len(role_rates) > 0:
            top_role = role_rates.idxmax()
            top_val = role_rates.max()
            critical_roles[dept] = f"{top_role} ({top_val:.1f}%)"
        else:
            critical_roles[dept] = "N/A"
            
    dept_group['CriticalRole'] = dept_group['DepartmentName'].map(critical_roles)
    dept_group['AttritionRate'] = dept_group['AttritionRate'].round(2)
    return dept_group.sort_values('AttritionRate', ascending=False)


def calculate_overtime_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes overtime vs non-overtime turnover and Chi-Square test of independence."""
    if len(df) == 0 or df['OverTime'].nunique() < 2:
        return {
            "ot_yes_rate": 0.0,
            "ot_no_rate": 0.0,
            "rate_diff": 0.0,
            "chi2_stat": 0.0,
            "p_value": 1.0,
            "significant": False
        }
        
    ot_yes = df[df['OverTime'] == 'Yes']
    ot_no = df[df['OverTime'] == 'No']
    
    rate_yes = (ot_yes['Attrition'] == 'Yes').mean() * 100 if len(ot_yes) > 0 else 0.0
    rate_no = (ot_no['Attrition'] == 'Yes').mean() * 100 if len(ot_no) > 0 else 0.0
    
    # Contingency Table
    contingency = pd.crosstab(df['OverTime'], df['Attrition'])
    if contingency.shape == (2, 2):
        chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
    else:
        chi2, p_val = 0.0, 1.0
        
    return {
        "ot_yes_rate": round(rate_yes, 2),
        "ot_no_rate": round(rate_no, 2),
        "rate_diff": round(rate_yes - rate_no, 2),
        "chi2_stat": round(chi2, 2),
        "p_value": p_val,
        "significant": bool(p_val < 0.05)
    }


def get_salary_band_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes turnover rates across 4 ordered compensation tiers."""
    order = ['Entry', 'Mid-Junior', 'Senior', 'Leadership']
    if len(df) == 0:
        return pd.DataFrame(columns=['SalaryBand', 'Headcount', 'Leavers', 'AttritionRate'])
        
    band_summary = df.groupby('SalaryBand').agg(
        Headcount=('EmployeeID', 'count'),
        Leavers=('Attrition', lambda x: (x == 'Yes').sum()),
        AttritionRate=('Attrition', lambda x: (x == 'Yes').mean() * 100)
    ).reindex(order).reset_index()
    
    band_summary['AttritionRate'] = band_summary['AttritionRate'].fillna(0.0).round(2)
    band_summary['Headcount'] = band_summary['Headcount'].fillna(0).astype(int)
    band_summary['Leavers'] = band_summary['Leavers'].fillna(0).astype(int)
    return band_summary


def get_role_level_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Returns 2D pivot table of JobRoleName (Y) x JobLevel (X) with turnover percentage."""
    if len(df) == 0:
        return pd.DataFrame()
        
    matrix = df.pivot_table(
        index='JobRoleName',
        columns='JobLevel',
        values='Attrition',
        aggfunc=lambda x: (x == 'Yes').mean() * 100,
        fill_value=0.0
    )
    return matrix.round(1)


def compute_satisfaction_correlations(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Computes correlation matrix between psychometric ratings and binary attrition."""
    sat_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance', 'RelationshipSatisfaction']
    if len(df) == 0:
        return pd.DataFrame(), {}
        
    calc_df = df[sat_cols].copy()
    calc_df['Attrition_Numeric'] = (df['Attrition'] == 'Yes').astype(int)
    
    corr_matrix = calc_df.corr(method='spearman').round(3)
    
    # Extract correlations with attrition
    att_corr = corr_matrix['Attrition_Numeric'].drop('Attrition_Numeric').to_dict()
    return corr_matrix, att_corr


def get_wlb_age_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tabulates Work-Life Balance scores against Age Brackets with turnover rates."""
    if len(df) == 0:
        return pd.DataFrame()
        
    matrix = df.pivot_table(
        index='WorkLifeBalance',
        columns='AgeBracket',
        values='Attrition',
        aggfunc=lambda x: (x == 'Yes').mean() * 100,
        fill_value=0.0
    )
    return matrix.round(1)


def get_tenure_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Computes attrition volume and rate % across discrete tenure bands."""
    order = ['Early-Tenure (<2 yr)', 'Mid-Tenure (2-5 yr)', 'Senior-Tenure (6-10 yr)', 'Veteran (10+ yr)']
    if len(df) == 0:
        return pd.DataFrame(columns=['TenureBand', 'Headcount', 'Leavers', 'AttritionRate'])
        
    summary = df.groupby('TenureBand').agg(
        Headcount=('EmployeeID', 'count'),
        Leavers=('Attrition', lambda x: (x == 'Yes').sum()),
        AttritionRate=('Attrition', lambda x: (x == 'Yes').mean() * 100)
    ).reindex(order).reset_index()
    
    summary['AttritionRate'] = summary['AttritionRate'].fillna(0.0).round(2)
    summary['Headcount'] = summary['Headcount'].fillna(0).astype(int)
    summary['Leavers'] = summary['Leavers'].fillna(0).astype(int)
    return summary


def compare_salary_hikes(df: pd.DataFrame) -> Dict[str, float]:
    """Compares median and mean annual salary hike percentages between stayers and leavers."""
    if len(df) == 0:
        return {"stayers_median": 0.0, "leavers_median": 0.0, "hike_diff": 0.0}
        
    stayers = df[df['Attrition'] == 'No']['PercentSalaryHike']
    leavers = df[df['Attrition'] == 'Yes']['PercentSalaryHike']
    
    stayers_med = float(stayers.median()) if len(stayers) > 0 else 0.0
    leavers_med = float(leavers.median()) if len(leavers) > 0 else 0.0
    
    return {
        "stayers_median": round(stayers_med, 1),
        "leavers_median": round(leavers_med, 1),
        "hike_diff": round(stayers_med - leavers_med, 1)
    }


def get_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Generates formatted descriptive statistics for key numerical columns."""
    cols = ['Age', 'MonthlyIncome', 'PercentSalaryHike', 'YearsAtCompany', 'DistanceFromHome']
    valid_cols = [c for c in cols if c in df.columns]
    if len(df) == 0 or len(valid_cols) == 0:
        return pd.DataFrame()
        
    desc = df[valid_cols].describe().T
    desc = desc[['count', 'mean', 'std', 'min', '50%', 'max']].rename(columns={'50%': 'median'})
    desc['mean'] = desc['mean'].round(1)
    desc['std'] = desc['std'].round(1)
    desc['median'] = desc['median'].round(1)
    return desc
