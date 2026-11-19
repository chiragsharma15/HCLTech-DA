"""
Main Application Entry Point & Executive Dashboard Router
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-06
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.analysis import compute_headline_kpis, get_monthly_trend, get_descriptive_stats
from src.charts import plot_attrition_trend_line
from src.ui import render_header, render_kpi_row, render_insight_box, render_section_header

# Global Streamlit Configuration
st.set_page_config(
    page_title="Employee Attrition Analysis | NovaTech",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Load cached database
    try:
        raw_df = load_data()
    except Exception as e:
        st.error(f"❌ Failed to load workforce database: {e}")
        st.info("Run `python src/generate_data.py` to regenerate the database if missing.")
        return

    # Render global sidebar filters
    filtered_df = render_sidebar_filters(raw_df)

    # 1. Page Header Banner
    render_header(
        title="Executive Overview & Workforce Turnover Health",
        subtitle="Empirical retention diagnostics and macro attrition monitoring for NovaTech Solutions Pvt. Ltd.",
        badge="Executive Overview"
    )

    # 2. Compute and Display Headline KPI Cards Row
    kpis = compute_headline_kpis(filtered_df)
    company_baseline = 21.28
    current_rate = kpis["raw_rate"]
    rate_diff = current_rate - company_baseline

    kpi_cards_data = [
        {
            "title": "Active Headcount",
            "value": kpis["total_employees"],
            "subtitle": f"Filtered workforce records",
            "delta": "Base: 1,250",
            "status": "neutral"
        },
        {
            "title": "Total Resignations",
            "value": kpis["total_leavers"],
            "subtitle": "Confirmed historical leavers",
            "delta": f"{kpis['total_leavers']} Departed",
            "status": "danger" if int(kpis["total_leavers"].replace(',', '')) > 200 else "neutral"
        },
        {
            "title": "Attrition Rate (%)",
            "value": kpis["attrition_rate"],
            "subtitle": f"Target benchmark: 12-15%",
            "delta": f"{rate_diff:+.1f}% vs Norm" if len(filtered_df) > 0 else "0.0%",
            "status": "danger" if current_rate >= 21.0 else ("warning" if current_rate >= 15.0 else "success")
        },
        {
            "title": "Avg Tenure of Leavers",
            "value": kpis["avg_leaver_tenure"],
            "subtitle": "Before voluntary departure",
            "delta": "Flight risk: <2.0 yrs",
            "status": "warning"
        }
    ]
    render_kpi_row(kpi_cards_data)

    # 3. Macro Insight Alert Box
    if current_rate > 21.0:
        render_insight_box(
            title="Elevated Enterprise Turnover Warning",
            text=f"The current filtered attrition rate stands at {kpis['attrition_rate']}, noticeably above the Indian IT-sector healthy target of 12-15%. Primary drivers identified include chronic overtime and early-tenure flight risk.",
            insight_type="danger"
        )
    else:
        render_insight_box(
            title="Workforce Stability Status",
            text="The selected employee cohort exhibits balanced turnover within acceptable corporate retention tolerances.",
            insight_type="success"
        )

    # 4. Temporal Attrition Trend Line
    render_section_header("Longitudinal Departure Trajectory", "Monthly employee resignation volumes across the 36-month observation window")
    trend_df = get_monthly_trend(filtered_df)
    fig_trend = plot_attrition_trend_line(trend_df)
    st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})

    # 5. Collapsible Descriptive Statistics Panel
    with st.expander("📊 View Descriptive Summary Statistics (Numerical Attributes)", expanded=False):
        st.markdown("<p style='font-size:0.85rem; color:#64748B;'>Distributional moments (Mean, Median, Standard Deviation, Quartiles) for core workforce metrics:</p>", unsafe_allow_html=True)
        stats_df = get_descriptive_stats(filtered_df)
        if len(stats_df) > 0:
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.info("No numerical records available for the active filter subset.")

if __name__ == "__main__":
    main()
