"""
Screen UI-05: Tenure Bands & Longitudinal Trends
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-10
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.analysis import get_tenure_breakdown, compare_salary_hikes
from src.charts import plot_tenure_band_bar, plot_salary_hike_boxplot, plot_yoy_department_trend
from src.ui import render_header, render_insight_box, render_section_header, render_navbar

st.set_page_config(page_title="Tenure & Trends | NovaTech", page_icon="📈", layout="wide")

def main():
    raw_df = load_data()
    filtered_df = render_sidebar_filters(raw_df)
    
    render_navbar("Trends")
    render_header(
        title="Tenure Analysis & Longitudinal Retention",
        subtitle="Tracking early-tenure flight risk, annual merit salary hike sensitivity, and multi-year benchmarks",
        badge="Longitudinal Retention"
    )
    
    render_insight_box(
        title="Onboarding Amortization Finding",
        text="Industry benchmarks establish that the <b>₹3–5 lakh cost</b> of recruitment and onboarding is not amortized if a new hire departs within 18–24 months. Early-tenure turnover represents pure financial loss that can be mitigated through early mentorship checkpoints.",
        insight_type="warning"
    )
    
    # ── Section 1 & 2: Tenure Bars & Salary Hike Boxplots ──
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_header("Tenure Band Distribution", "Highlighting early-career vulnerability (<2 years of completed service)")
        tenure_df = get_tenure_breakdown(filtered_df)
        fig_tenure = plot_tenure_band_bar(tenure_df)
        st.plotly_chart(fig_tenure, use_container_width=True, config={'displayModeBar': False})
        
    with col2:
        render_section_header("Merit Salary Hike Sensitivity", "Plotly box plot comparing annual increment distributions (Stayers vs. Leavers)")
        hike_stats = compare_salary_hikes(filtered_df)
        fig_box = plot_salary_hike_boxplot(filtered_df)
        st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown(f"""
            <div style="background-color: #F8FAFC; border-left: 4px solid #0284C7; padding: 10px; border-radius: 4px; font-size: 0.85rem;">
                <b>Increment Differential:</b> Retained staff enjoy a median hike of <b>{hike_stats['stayers_median']}%</b> vs. <b>{hike_stats['leavers_median']}%</b> for departed employees (a <b>-{hike_stats['hike_diff']}% gap</b>). Sub-13% salary hikes strongly correlate with departure.
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    # ── Section 3: Multi-Year Longitudinal Department Trends ──
    render_section_header("Multi-Year Longitudinal Department Benchmark", "Annual attrition rate (%) progression across calendar cohort years")
    fig_yoy = plot_yoy_department_trend(filtered_df)
    st.plotly_chart(fig_yoy, use_container_width=True, config={'displayModeBar': False})

if __name__ == "__main__":
    main()
