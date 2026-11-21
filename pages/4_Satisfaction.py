"""
Screen UI-04: Psychometric & Satisfaction Analytics
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-09
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.analysis import compute_satisfaction_correlations, get_wlb_age_matrix
from src.charts import plot_satisfaction_correlation_heatmap, plot_wlb_age_heatmap
from src.ui import render_header, render_insight_box, render_section_header, render_navbar

st.set_page_config(page_title="Satisfaction & Engagement | NovaTech", page_icon="❤️", layout="wide")

def main():
    raw_df = load_data()
    filtered_df = render_sidebar_filters(raw_df)
    
    render_navbar("Satisfaction")
    render_header(
        title="Psychometric & Workplace Satisfaction Analytics",
        subtitle="Evaluating controllable workplace environment ratings and work-life balance perceptions",
        badge="Engagement Analytics"
    )
    
    render_insight_box(
        title="Actionable Controllability",
        text="Unlike immutable demographic factors (Age, Gender) or municipal commute distance, <b>Job Satisfaction</b> and <b>Work-Life Balance</b> are directly addressable through management mentorship, flexible scheduling, and workload calibration.",
        insight_type="info"
    )
    
    # ── Section 1: Correlation Matrix & Rating Breakdown ──
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_header("Psychometric Correlation Matrix", "Spearman rank correlation coefficients between survey factors and turnover")
        corr_matrix, att_corrs = compute_satisfaction_correlations(filtered_df)
        fig_corr = plot_satisfaction_correlation_heatmap(corr_matrix)
        st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
        
    with col2:
        render_section_header("Turnover by Likert Rating (1-4)", "Impact of discrete survey scores on departure proportion")
        if len(filtered_df) > 0:
            sat_breakdown = filtered_df.groupby('JobSatisfaction').agg(
                Total=('EmployeeID', 'count'),
                Leavers=('Attrition', lambda x: (x == 'Yes').sum()),
                Rate=('Attrition', lambda x: (x == 'Yes').mean() * 100)
            ).reset_index()
            
            sat_breakdown['Rate'] = sat_breakdown['Rate'].round(1)
            sat_breakdown['Rating Description'] = sat_breakdown['JobSatisfaction'].map({
                1: '1 - Low Satisfaction',
                2: '2 - Medium Satisfaction',
                3: '3 - High Satisfaction',
                4: '4 - Very High Satisfaction'
            })
            
            st.dataframe(
                sat_breakdown[['Rating Description', 'Total', 'Leavers', 'Rate']].rename(columns={'Rate': 'Attrition Rate (%)'}),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Attrition Rate (%)": st.column_config.ProgressColumn(
                        "Attrition Rate (%)",
                        format="%.1f%%",
                        min_value=0,
                        max_value=40
                    )
                }
            )
            st.markdown("""
                <p style="font-size:0.85rem; color:#475569; margin-top:10px;">
                    <b>Key Takeaway:</b> Employees reporting a <b>Score 1 (Low)</b> face over <b>3x higher departure risk</b> compared to employees reporting a <b>Score 4 (Very High)</b>.
                </p>
            """, unsafe_allow_html=True)
        else:
            st.info("No records matching active filters.")
            
    st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    # ── Section 2: WLB vs Age Cohort Matrix ──
    render_section_header("Work-Life Balance Across Age Demographics", "Cross-tabulation of Work-Life Balance ratings (1-4) by Employee Age Bracket")
    wlb_matrix = get_wlb_age_matrix(filtered_df)
    fig_wlb = plot_wlb_age_heatmap(wlb_matrix)
    st.plotly_chart(fig_wlb, use_container_width=True, config={'displayModeBar': False})

if __name__ == "__main__":
    main()
