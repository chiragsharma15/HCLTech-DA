"""
Global Sidebar Filter Engine with Session State Persistence
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-05
"""

import streamlit as st
import pandas as pd
from typing import Tuple

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders global interactive sidebar filters with st.session_state persistence.
    Returns filtered DataFrame subset and manages reset events.
    """
    st.sidebar.markdown("""
        <div style="padding: 10px 0 15px 0; border-bottom: 2px solid #E2E8F0; margin-bottom: 15px;">
            <h3 style="color: #1B3A5C; font-weight: 800; margin: 0; font-size: 1.15rem;">WORKFORCE FILTERS</h3>
            <p style="color: #64748B; font-size: 0.8rem; margin: 2px 0 0 0;">Slice across multiple organizational dimensions</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. Department Multi-select
    all_depts = sorted(df['DepartmentName'].dropna().unique().tolist())
    selected_depts = st.sidebar.multiselect(
        "Department:",
        options=all_depts,
        default=st.session_state.get('filter_dept', []),
        key='filter_dept',
        help="Select one or more departments to isolate analytics."
    )
    
    # Filter available roles based on department selection
    if selected_depts:
        available_roles = sorted(df[df['DepartmentName'].isin(selected_depts)]['JobRoleName'].dropna().unique().tolist())
    else:
        available_roles = sorted(df['JobRoleName'].dropna().unique().tolist())
        
    # 2. Job Role Multi-select
    selected_roles = st.sidebar.multiselect(
        "Job Role Designation:",
        options=available_roles,
        default=st.session_state.get('filter_role', []),
        key='filter_role'
    )
    
    # 3. OverTime Radio Filter
    ot_options = ['All', 'Yes', 'No']
    selected_ot = st.sidebar.radio(
        "Overtime Obligation:",
        options=ot_options,
        index=ot_options.index(st.session_state.get('filter_ot', 'All')),
        key='filter_ot',
        horizontal=True
    )
    
    # 4. Age Slider
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())
    selected_age = st.sidebar.slider(
        "Employee Age Range:",
        min_value=min_age,
        max_value=max_age,
        value=st.session_state.get('filter_age', (min_age, max_age)),
        key='filter_age'
    )
    
    # 5. Salary Band Multi-select
    all_bands = ['Entry', 'Mid-Junior', 'Senior', 'Leadership']
    selected_bands = st.sidebar.multiselect(
        "Salary Band:",
        options=all_bands,
        default=st.session_state.get('filter_band', []),
        key='filter_band'
    )
    
    # 6. Gender Filter
    all_genders = ['Male', 'Female']
    selected_genders = st.sidebar.multiselect(
        "Gender:",
        options=all_genders,
        default=st.session_state.get('filter_gender', []),
        key='filter_gender'
    )
    
    # Reset Filters Button
    st.sidebar.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state['filter_dept'] = []
        st.session_state['filter_role'] = []
        st.session_state['filter_ot'] = 'All'
        st.session_state['filter_age'] = (min_age, max_age)
        st.session_state['filter_band'] = []
        st.session_state['filter_gender'] = []
        st.rerun()
        
    # ── Apply Filter Logic ──
    filtered_df = df.copy()
    active_filters_count = 0
    
    if selected_depts:
        filtered_df = filtered_df[filtered_df['DepartmentName'].isin(selected_depts)]
        active_filters_count += 1
        
    if selected_roles:
        filtered_df = filtered_df[filtered_df['JobRoleName'].isin(selected_roles)]
        active_filters_count += 1
        
    if selected_ot != 'All':
        filtered_df = filtered_df[filtered_df['OverTime'] == selected_ot]
        active_filters_count += 1
        
    if selected_age != (min_age, max_age):
        filtered_df = filtered_df[filtered_df['Age'].between(selected_age[0], selected_age[1])]
        active_filters_count += 1
        
    if selected_bands:
        filtered_df = filtered_df[filtered_df['SalaryBand'].isin(selected_bands)]
        active_filters_count += 1
        
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
        active_filters_count += 1
        
    # Active Filter Status Badge
    badge_color = "#E11D48" if active_filters_count > 0 else "#64748B"
    st.sidebar.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.8rem; text-align: center;">
            <span style="font-weight: 700; color: {badge_color};">Active Filters: {active_filters_count}</span><br>
            <span style="color: #475569;">Matching Records: <b>{len(filtered_df):,}</b> of {len(df):,}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if len(filtered_df) == 0:
        st.warning("⚠️ No employee records match the active filter criteria. Please broaden your selection.")
        
    return filtered_df
