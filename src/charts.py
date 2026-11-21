"""
Plotly Visualisation Factory
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-04
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

NAVY_PRIMARY = "#1B3A5C"
ROSE_DANGER = "#E11D48"
SKY_SECONDARY = "#0284C7"
EMERALD_SAFE = "#10B981"
AMBER_WARN = "#F59E0B"
SLATE_TEXT = "#1E293B"

LAYOUT_DEFAULTS = dict(
    font=dict(family="Calibri, sans-serif", color=SLATE_TEXT, size=12),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=30, t=50, b=40),
)

def plot_attrition_trend_line(trend_df: pd.DataFrame) -> go.Figure:
    """Generates 36-month departure trend line with area shading."""
    fig = go.Figure()
    if len(trend_df) == 0:
        fig.add_annotation(text="No departure records matching active filters", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig.add_trace(go.Scatter(
        x=trend_df['YearMonth'],
        y=trend_df['LeaversCount'],
        mode='lines+markers',
        name='Monthly Departures',
        line=dict(color=ROSE_DANGER, width=3),
        marker=dict(size=6, color=NAVY_PRIMARY),
        fill='tozeroy',
        fillcolor='rgba(225, 29, 72, 0.08)',
        hovertemplate='<b>%{x}</b><br>Resignations: %{y} employees<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Monthly Workforce Departure Trend (36-Month Timeline)</b>",
        xaxis=dict(title="Departure Month", showgrid=True, gridcolor="#F1F5F9", tickangle=-45),
        yaxis=dict(title="Employee Departures", showgrid=True, gridcolor="#F1F5F9"),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_department_ranking_bar(dept_df: pd.DataFrame, company_avg: float = 21.28) -> go.Figure:
    """Generates ranked horizontal bar chart comparing department turnover rates."""
    fig = go.Figure()
    if len(dept_df) == 0:
        fig.add_annotation(text="No department data available", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    df_sorted = dept_df.sort_values('AttritionRate', ascending=True)
    colors = [ROSE_DANGER if r >= company_avg else NAVY_PRIMARY for r in df_sorted['AttritionRate']]
    
    fig.add_trace(go.Bar(
        y=df_sorted['DepartmentName'],
        x=df_sorted['AttritionRate'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(0,0,0,0.1)', width=1)),
        text=[f"{r:.1f}%" for r in df_sorted['AttritionRate']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Attrition Rate: %{x:.2f}%<extra></extra>'
    ))
    
    # Add vertical line for company benchmark
    fig.add_vline(
        x=company_avg, line_dash="dash", line_color=AMBER_WARN, line_width=2,
        annotation_text=f"Company Avg ({company_avg:.1f}%)", annotation_position="top right"
    )
    
    fig.update_layout(
        title="<b>Department Attrition Rate (%) Comparison & Ranking</b>",
        xaxis=dict(title="Attrition Rate (%)", showgrid=True, gridcolor="#F1F5F9", range=[0, max(dept_df['AttritionRate'].max() + 5, 35)]),
        yaxis=dict(title="", showgrid=False),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_overtime_comparison_bar(stats_dict: Dict[str, Any]) -> go.Figure:
    """Generates grouped bar chart comparing overtime vs non-overtime turnover."""
    categories = ['OverTime: Yes', 'OverTime: No']
    rates = [stats_dict.get('ot_yes_rate', 0.0), stats_dict.get('ot_no_rate', 0.0)]
    colors = [ROSE_DANGER, NAVY_PRIMARY]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=rates,
            marker_color=colors,
            text=[f"{r:.1f}%" for r in rates],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Attrition Rate: %{y:.2f}%<extra></extra>',
            width=[0.45, 0.45]
        )
    ])
    
    fig.update_layout(
        title=f"<b>Overtime Attrition Impact (Chi2: {stats_dict.get('chi2_stat', 0.0)}, p < 0.001)</b>",
        yaxis=dict(title="Attrition Rate (%)", showgrid=True, gridcolor="#F1F5F9", range=[0, 40]),
        xaxis=dict(title=""),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_salary_band_bar(band_df: pd.DataFrame) -> go.Figure:
    """Generates ordered categorical bar chart across compensation tiers."""
    fig = go.Figure()
    if len(band_df) == 0:
        fig.add_annotation(text="No salary band data", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig.add_trace(go.Bar(
        x=band_df['SalaryBand'],
        y=band_df['AttritionRate'],
        marker_color=[ROSE_DANGER, SKY_SECONDARY, NAVY_PRIMARY, EMERALD_SAFE],
        text=[f"{r:.1f}%" for r in band_df['AttritionRate']],
        textposition='outside',
        hovertemplate='<b>%{x} Band</b><br>Attrition Rate: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Attrition Rate (%) by Compensation Tier</b>",
        xaxis=dict(title="Salary Band", showgrid=False),
        yaxis=dict(title="Attrition Rate (%)", showgrid=True, gridcolor="#F1F5F9", range=[0, 40]),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_role_level_heatmap(matrix_df: pd.DataFrame) -> go.Figure:
    """Generates 2D interactive heatmap for Job Role x Seniority Job Level."""
    if len(matrix_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No role hierarchy data available", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig = go.Figure(data=go.Heatmap(
        z=matrix_df.values,
        x=[f"Level {col}" for col in matrix_df.columns],
        y=matrix_df.index,
        colorscale='Reds',
        text=[[f"{v:.1f}%" if v > 0 else "-" for v in row] for row in matrix_df.values],
        texttemplate="%{text}",
        textfont={"size": 10},
        colorbar=dict(title="Rate %"),
        hovertemplate='<b>%{y}</b><br>%{x}<br>Attrition Rate: %{z:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Job Role x Seniority Job Level Attrition Vulnerability Matrix</b>",
        xaxis=dict(title="Hierarchy Seniority Level"),
        yaxis=dict(title="Job Designation", automargin=True),
        height=480,
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_satisfaction_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Generates correlation matrix heatmap for psychometric satisfaction metrics."""
    if len(corr_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No correlation data", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale='Blues',
        reversescale=True,
        text=[[f"{v:.2f}" for v in row] for row in corr_df.values],
        texttemplate="%{text}",
        colorbar=dict(title="Spearman rho"),
        zmin=-0.4, zmax=0.4
    ))
    
    fig.update_layout(
        title="<b>Psychometric Ratings & Attrition Correlation Matrix</b>",
        xaxis=dict(tickangle=-25),
        height=400,
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_wlb_age_heatmap(matrix_df: pd.DataFrame) -> go.Figure:
    """Generates Work-Life Balance vs Age Cohort cross-tabulation heatmap."""
    if len(matrix_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No WLB x Age data", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig = go.Figure(data=go.Heatmap(
        z=matrix_df.values,
        x=matrix_df.columns,
        y=[f"Rating {idx}" for idx in matrix_df.index],
        colorscale='YlOrRd',
        text=[[f"{v:.1f}%" if v > 0 else "-" for v in row] for row in matrix_df.values],
        texttemplate="%{text}",
        colorbar=dict(title="Rate %")
    ))
    
    fig.update_layout(
        title="<b>Work-Life Balance Rating vs Age Cohort Attrition Rate (%)</b>",
        xaxis=dict(title="Age Cohort"),
        yaxis=dict(title="Work-Life Balance Score (1=Bad to 4=Best)"),
        height=380,
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_tenure_band_bar(tenure_df: pd.DataFrame) -> go.Figure:
    """Generates tenure band attrition bar chart highlighting early-tenure flight risk."""
    fig = go.Figure()
    if len(tenure_df) == 0:
        fig.add_annotation(text="No tenure data", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    colors = [ROSE_DANGER if 'Early' in b else NAVY_PRIMARY for b in tenure_df['TenureBand']]
    
    fig.add_trace(go.Bar(
        x=tenure_df['TenureBand'],
        y=tenure_df['AttritionRate'],
        marker_color=colors,
        text=[f"{r:.1f}%" for r in tenure_df['AttritionRate']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Attrition Rate: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Attrition Rate (%) by Organisational Tenure Band (Highlighting <2 Yrs)</b>",
        xaxis=dict(title="Tenure Band"),
        yaxis=dict(title="Attrition Rate (%)", range=[0, 35], showgrid=True, gridcolor="#F1F5F9"),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_salary_hike_boxplot(df: pd.DataFrame) -> go.Figure:
    """Generates box plots comparing PercentSalaryHike between Stayers and Leavers."""
    fig = go.Figure()
    if len(df) == 0:
        fig.add_annotation(text="No salary hike data", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig.add_trace(go.Box(
        y=df[df['Attrition'] == 'No']['PercentSalaryHike'],
        name='Retained Staff',
        marker_color=NAVY_PRIMARY,
        boxmean=True
    ))
    
    fig.add_trace(go.Box(
        y=df[df['Attrition'] == 'Yes']['PercentSalaryHike'],
        name='Departed Staff',
        marker_color=ROSE_DANGER,
        boxmean=True
    ))
    
    fig.update_layout(
        title="<b>Annual Merit Salary Hike (%) Distribution (Stayers vs. Leavers)</b>",
        yaxis=dict(title="Salary Hike (%)", showgrid=True, gridcolor="#F1F5F9"),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_yoy_department_trend(df: pd.DataFrame) -> go.Figure:
    """Generates multi-line longitudinal department attrition trend chart across calendar years."""
    fig = go.Figure()
    if len(df) == 0:
        fig.add_annotation(text="No longitudinal data", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    df_calc = df.copy()
    df_calc['Year'] = df_calc['DateOfJoining'].str.slice(0, 4)
    
    # Calculate year-wise department attrition
    yoy_group = df_calc.groupby(['Year', 'DepartmentName']).agg(
        Rate=('Attrition', lambda x: (x == 'Yes').mean() * 100)
    ).reset_index()
    
    for dept in yoy_group['DepartmentName'].unique():
        sub = yoy_group[yoy_group['DepartmentName'] == dept]
        fig.add_trace(go.Scatter(
            x=sub['Year'],
            y=sub['Rate'],
            mode='lines+markers',
            name=dept
        ))
        
    fig.update_layout(
        title="<b>Multi-Year Longitudinal Department Attrition Trend</b>",
        xaxis=dict(title="Joining Cohort Year"),
        yaxis=dict(title="Attrition Rate (%)", showgrid=True, gridcolor="#F1F5F9"),
        **LAYOUT_DEFAULTS
    )
    return fig


def plot_demographic_sunburst(df: pd.DataFrame) -> go.Figure:
    """Generates hierarchical Sunburst chart (Department -> Role -> OverTime -> Attrition)."""
    if len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No records match active filters", showarrow=False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
        
    fig = px.sunburst(
        df,
        path=['DepartmentName', 'JobRoleName', 'OverTime', 'Attrition'],
        color='Attrition',
        color_discrete_map={'Yes': ROSE_DANGER, 'No': SKY_SECONDARY},
        title="<b>Hierarchical Workforce Breakdown & Departure Flow</b>"
    )
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=500)
    return fig
