"""
Screen UI-03: Workforce Deep-Dive & Overtime Burnout
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-08
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.analysis import calculate_overtime_stats, get_salary_band_summary, get_role_level_matrix
from src.charts import plot_overtime_comparison_bar, plot_salary_band_bar, plot_role_level_heatmap
from src.ui import render_header, render_insight_box, render_section_header

st.set_page_config(page_title="Workforce Deep-Dive | NovaTech", page_icon="🔍", layout="wide")

def main():
    raw_df = load_data()
    filtered_df = render_sidebar_filters(raw_df)
    
    render_header(
        title="Workforce Deep-Dive: Overtime & Compensation",
        subtitle="Empirical evaluation of chronic overtime obligations and compensation tier vulnerability",
        badge="Deep-Dive Diagnostics"
    )
    
    # ── Section 1 & 2: Overtime and Salary Bands side-by-side ──
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_header("Overtime Burnout Impact", "Chi-Square test of independence on mandatory overtime obligations")
        ot_stats = calculate_overtime_stats(filtered_df)
        fig_ot = plot_overtime_comparison_bar(ot_stats)
        st.plotly_chart(fig_ot, use_container_width=True, config={'displayModeBar': False})
        
        # Statistical summary card
        sig_text = "Statistically Significant (p < 0.05)" if ot_stats["significant"] else "Not Statistically Significant"
        st.markdown(f"""
            <div style="background-color: #F8FAFC; border-left: 4px solid #E11D48; padding: 12px; border-radius: 4px; font-size: 0.85rem;">
                <b>Chi-Square Independence Test:</b><br>
                Test Statistic: <code>{ot_stats['chi2_stat']}</code> | p-value: <code>{ot_stats['p_value']:.4e}</code><br>
                <b>Outcome:</b> <span style="color: #E11D48; font-weight: bold;">{sig_text}</span> — Overtime employees face a <b>+{ot_stats['rate_diff']}%</b> departure premium.
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        render_section_header("Compensation Tier Turnover", "Step-function turnover progression across 4 defined salary bands")
        band_df = get_salary_band_summary(filtered_df)
        fig_band = plot_salary_band_bar(band_df)
        st.plotly_chart(fig_band, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("""
            <div style="background-color: #F8FAFC; border-left: 4px solid #1B3A5C; padding: 12px; border-radius: 4px; font-size: 0.85rem;">
                <b>Compensation Band Breakdown:</b><br>
                Entry (<₹25k) and Mid-Junior (₹25k–₹50k) staff represent over 65% of all corporate turnover. Retention bonuses must target early-career brackets rather than uniform executive adjustments.
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    # ── Section 3: Job Role x Level Heatmap ──
    render_section_header("Career Hierarchy Matrix", "Granular cross-tabulation of Job Designation (Y) by Seniority Job Level (1 to 5)")
    role_matrix = get_role_level_matrix(filtered_df)
    fig_matrix = plot_role_level_heatmap(role_matrix)
    st.plotly_chart(fig_matrix, use_container_width=True, config={'displayModeBar': False})

if __name__ == "__main__":
    main()
