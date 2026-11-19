"""
Screen UI-02: Department Turnover & Vulnerability Rankings
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-07
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.analysis import get_department_summary, compute_headline_kpis
from src.charts import plot_department_ranking_bar
from src.ui import render_header, render_insight_box, render_section_header

st.set_page_config(page_title="Department Analysis | NovaTech", page_icon="🏢", layout="wide")

def main():
    raw_df = load_data()
    filtered_df = render_sidebar_filters(raw_df)
    
    render_header(
        title="Departmental Turnover Comparison & Ranking",
        subtitle="Identifying high-vulnerability business units to target retention interventions",
        badge="Department Analysis"
    )
    
    # Department summary aggregations
    dept_df = get_department_summary(filtered_df)
    company_kpis = compute_headline_kpis(filtered_df)
    
    # 1. Insight callout
    if len(dept_df) > 0:
        highest_dept = dept_df.iloc[0]['DepartmentName']
        highest_rate = dept_df.iloc[0]['AttritionRate']
        lowest_dept = dept_df.iloc[-1]['DepartmentName']
        lowest_rate = dept_df.iloc[-1]['AttritionRate']
        
        render_insight_box(
            title="Departmental Disparity Finding",
            text=f"Turnover varies significantly across business units. <b>{highest_dept}</b> experiences the highest turnover at <b>{highest_rate:.1f}%</b>, whereas <b>{lowest_dept}</b> remains the most stable unit at <b>{lowest_rate:.1f}%</b>. Blanket compensation policies fail to address this departmental divergence.",
            insight_type="warning"
        )
        
    # 2. Ranked Bar Chart
    render_section_header("Cross-Departmental Attrition Ranking", "Ranked from highest turnover rate to lowest against company benchmark")
    fig_dept = plot_department_ranking_bar(dept_df, company_avg=company_kpis.get("raw_rate", 21.28))
    st.plotly_chart(fig_dept, use_container_width=True, config={'displayModeBar': False})
    
    # 3. Departmental Metric Breakdown Table
    render_section_header("Unit Breakdown & Critical Risk Role Roster", "Summary metrics with most vulnerable designations per operational unit")
    if len(dept_df) > 0:
        display_df = dept_df.rename(columns={
            'DepartmentName': 'Department',
            'TotalHeadcount': 'Active Headcount',
            'LeaverCount': 'Total Leavers',
            'AttritionRate': 'Attrition Rate (%)',
            'CriticalRole': 'Highest Turnover Designation'
        })
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Attrition Rate (%)": st.column_config.ProgressColumn(
                    "Attrition Rate (%)",
                    help="Turnover percentage for the department",
                    format="%.1f%%",
                    min_value=0,
                    max_value=35,
                ),
            }
        )
    else:
        st.info("No department records available matching the active filter selection.")

if __name__ == "__main__":
    main()
