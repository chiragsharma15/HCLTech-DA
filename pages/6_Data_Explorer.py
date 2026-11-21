"""
Screen UI-06: Multi-Factor Risk Profiler & Tabular Data Explorer
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-11
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.filters import render_sidebar_filters
from src.charts import plot_demographic_sunburst
from src.utils import export_to_csv, export_to_excel
from src.ui import render_header, render_insight_box, render_section_header, render_navbar

st.set_page_config(page_title="Data Explorer & Export | NovaTech", page_icon="📁", layout="wide")

def main():
    raw_df = load_data()
    filtered_df = render_sidebar_filters(raw_df)
    
    render_navbar("Explorer")
    render_header(
        title="Intersectional Risk Profiler & Data Explorer",
        subtitle="Exploring compound demographic vulnerabilities and exporting curated analytical subsets",
        badge="Self-Service Explorer"
    )
    
    # ── Subsection 1: Subset Summary & Sunburst ──
    total_subset = len(filtered_df)
    subset_leavers = (filtered_df['Attrition'] == 'Yes').sum() if total_subset > 0 else 0
    subset_rate = (subset_leavers / total_subset * 100) if total_subset > 0 else 0.0
    
    col_card, col_action = st.columns([3, 1])
    with col_card:
        card_color = "#E11D48" if subset_rate >= 25.0 else ("#1B3A5C" if subset_rate >= 15.0 else "#10B981")
        st.markdown(f"""
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid {card_color}; padding: 16px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: bold;">Active Filtered Subset Health</div>
                <div style="font-size: 1.8rem; font-weight: 900; color: #1E293B; margin: 4px 0;">{total_subset:,} Employees <span style="font-size: 1.1rem; color: {card_color};">({subset_rate:.2f}% Attrition)</span></div>
                <div style="font-size: 0.85rem; color: #475569;">Confirmed Departures: <b>{subset_leavers:,}</b> | Benchmark Variance: <b>{subset_rate - 21.28:+.1f}%</b></div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_action:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        csv_data = export_to_csv(filtered_df)
        st.download_button(
            label="📥 Export Filtered CSV",
            data=csv_data,
            file_name="novatech_filtered_attrition_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Download Master Excel workbook if under 5,000 rows
        if total_subset <= 5000:
            excel_data = export_to_excel(filtered_df)
            st.download_button(
                label="📊 Export Master Excel",
                data=excel_data,
                file_name="novatech_filtered_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
    st.markdown("<hr style='margin: 25px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    # ── Subsection 2: Sunburst Chart ──
    render_section_header("Hierarchical Flow & Department Sub-branching", "Click concentric rings to drill into Department -> Role -> Overtime subsets")
    fig_sun = plot_demographic_sunburst(filtered_df)
    st.plotly_chart(fig_sun, use_container_width=True, config={'displayModeBar': False})
    
    # ── Subsection 3: Tabular Record Explorer ──
    render_section_header("Interactive Tabular Records (Active Filter Subset)", "Full analytical attributes viewable with in-column sorting and filtering")
    if total_subset > 0:
        display_columns = [
            'EmployeeID', 'Age', 'Gender', 'MaritalStatus', 'DepartmentName', 'JobRoleName',
            'JobLevel', 'MonthlyIncome', 'SalaryBand', 'OverTime', 'YearsAtCompany',
            'DistanceFromHome', 'JobSatisfaction', 'WorkLifeBalance', 'Attrition'
        ]
        valid_cols = [c for c in display_columns if c in filtered_df.columns]
        st.dataframe(
            filtered_df[valid_cols],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No records to display. Try broadening your filter selection.")

if __name__ == "__main__":
    main()
