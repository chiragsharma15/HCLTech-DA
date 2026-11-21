"""
Global Sidebar Filter Engine with Session State Persistence
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-05
"""

import streamlit as st
import pandas as pd
from typing import Tuple


def _reset_all_filters(min_age: int, max_age: int) -> None:
    """
    Streamlit on_click callback to safely reset all filter keys in session_state.
    Executes BEFORE widgets are rendered in the next run, preventing StreamlitAPIException.
    """
    st.session_state['filter_dept'] = []
    st.session_state['filter_role'] = []
    st.session_state['filter_ot'] = 'All'
    st.session_state['filter_age'] = (min_age, max_age)
    st.session_state['filter_band'] = []
    st.session_state['filter_gender'] = []


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders compact global interactive sidebar filters with st.session_state persistence.
    Designed for zero-scroll accessibility with instant top-level reset action.
    """
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())

    # Initialize all session keys safely if not present
    if 'filter_dept' not in st.session_state:
        st.session_state['filter_dept'] = []
    if 'filter_role' not in st.session_state:
        st.session_state['filter_role'] = []
    if 'filter_ot' not in st.session_state:
        st.session_state['filter_ot'] = 'All'
    if 'filter_age' not in st.session_state:
        st.session_state['filter_age'] = (min_age, max_age)
    if 'filter_band' not in st.session_state:
        st.session_state['filter_band'] = []
    if 'filter_gender' not in st.session_state:
        st.session_state['filter_gender'] = []

    # Compact CSS injection to ensure all filters fit comfortably on screen without scrolling
    st.sidebar.markdown("""
        <style>
        /* Compact Sidebar - No Scrolling Needed */
        section[data-testid="stSidebar"] {
            padding-top: 0.5rem !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
            padding-top: 0.12rem !important;
            padding-bottom: 0.12rem !important;
        }
        section[data-testid="stSidebar"] .stMultiSelect,
        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stSlider {
            margin-bottom: -0.25rem !important;
        }
        section[data-testid="stSidebar"] label p {
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            color: #1B3A5C !important;
            margin-bottom: 2px !important;
        }
        section[data-testid="stSidebar"] .stButton button {
            border-radius: 6px !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            padding: 2px 8px !important;
            height: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── Top Sidebar Header with Instant Reset Button ──
    header_col1, header_col2 = st.sidebar.columns([3, 2])
    with header_col1:
        st.markdown("""
            <div style="padding-top: 4px;">
                <span style="color: #1B3A5C; font-weight: 800; font-size: 0.95rem; letter-spacing: 0.5px;">FILTERS</span>
                <span style="color: #64748B; font-size: 0.72rem; display: block; margin-top: -2px;">Workforce Slicing</span>
            </div>
        """, unsafe_allow_html=True)
    with header_col2:
        st.button(
            "🔄 Reset All",
            on_click=_reset_all_filters,
            args=(min_age, max_age),
            key="btn_reset_top",
            help="Reset all filters back to default enterprise cohort",
            use_container_width=True
        )

    # 1. Department Multi-select
    all_depts = sorted(df['DepartmentName'].dropna().unique().tolist())
    selected_depts = st.sidebar.multiselect(
        "Department:",
        options=all_depts,
        key='filter_dept',
        help="Select one or more departments to isolate analytics."
    )

    # Filter available roles based on department selection
    if selected_depts:
        available_roles = sorted(df[df['DepartmentName'].isin(selected_depts)]['JobRoleName'].dropna().unique().tolist())
    else:
        available_roles = sorted(df['JobRoleName'].dropna().unique().tolist())

    # Sanitize selected roles to prevent invalid state if department changes
    valid_roles = [r for r in st.session_state.get('filter_role', []) if r in available_roles]
    if valid_roles != st.session_state.get('filter_role', []):
        st.session_state['filter_role'] = valid_roles

    # 2. Job Role Multi-select
    selected_roles = st.sidebar.multiselect(
        "Job Role Designation:",
        options=available_roles,
        key='filter_role'
    )

    # 3. OverTime Radio Filter
    ot_options = ['All', 'Yes', 'No']
    selected_ot = st.sidebar.radio(
        "Overtime Obligation:",
        options=ot_options,
        key='filter_ot',
        horizontal=True
    )

    # 4. Age Slider
    selected_age = st.sidebar.slider(
        "Employee Age Range:",
        min_value=min_age,
        max_value=max_age,
        key='filter_age'
    )

    # 5. Salary Band Multi-select
    all_bands = ['Entry', 'Mid-Junior', 'Senior', 'Leadership']
    selected_bands = st.sidebar.multiselect(
        "Salary Band:",
        options=all_bands,
        key='filter_band'
    )

    # 6. Gender Filter
    all_genders = ['Male', 'Female']
    selected_genders = st.sidebar.multiselect(
        "Gender:",
        options=all_genders,
        key='filter_gender'
    )

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

    # Active Filter Status Badge & Bottom Reset Shortcut
    badge_color = "#E11D48" if active_filters_count > 0 else "#64748B"
    st.sidebar.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 6px 10px; border-radius: 6px; margin-top: 8px; font-size: 0.75rem; text-align: center;">
            <span style="font-weight: 700; color: {badge_color};">Active Filters: {active_filters_count}</span> &bull; 
            <span style="color: #475569;">Matches: <b>{len(filtered_df):,}</b> of {len(df):,}</span>
        </div>
    """, unsafe_allow_html=True)

    if len(filtered_df) == 0:
        st.warning("⚠️ No employee records match the active filter criteria. Please broaden your selection.")

    return filtered_df
