"""
UI Component Factory for Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Step 12 - UI Framework
Provides reusable Tailwind-styled components for Streamlit dashboards.
"""

import streamlit as st
import streamlit.components.v1 as components

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def render_header(title: str, subtitle: str, badge: str = "HR Analytics Platform") -> None:
    """Renders a responsive corporate Tailwind header banner."""
    html_code = f"""
    {TAILWIND_CDN}
    <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 text-white p-6 rounded-2xl shadow-xl mb-6 border border-slate-800">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
                <div class="flex items-center gap-2 mb-2">
                    <span class="bg-blue-600 text-white text-xs font-semibold px-2.5 py-1 rounded-full uppercase tracking-wider">{badge}</span>
                    <span class="text-slate-400 text-xs">NovaTech Solutions | EAA-2025</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">{title}</h1>
                <p class="text-slate-300 text-sm mt-1">{subtitle}</p>
            </div>
            <div class="flex items-center gap-3 text-xs text-slate-300 bg-slate-800/60 px-4 py-2 rounded-xl border border-slate-700/50">
                <div class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></div>
                <span>Live SQLite Engine</span>
            </div>
        </div>
    </div>
    """
    components.html(html_code, height=130)


def render_kpi_row(kpis: list) -> None:
    """
    Renders a responsive 4-column row of Tailwind KPI cards.
    kpis: list of dicts with keys: title, value, subtitle, delta, status ('neutral', 'danger', 'success')
    """
    cards_html = ""
    for k in kpis:
        status = k.get("status", "neutral")
        if status == "danger":
            badge_class = "bg-rose-50 text-rose-700 border-rose-200"
            border_accent = "border-t-4 border-rose-600"
            dot_color = "bg-rose-600"
        elif status == "success":
            badge_class = "bg-emerald-50 text-emerald-700 border-emerald-200"
            border_accent = "border-t-4 border-emerald-600"
            dot_color = "bg-emerald-600"
        else:
            badge_class = "bg-blue-50 text-blue-700 border-blue-200"
            border_accent = "border-t-4 border-blue-700"
            dot_color = "bg-blue-600"
            
        cards_html += f"""
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 {border_accent} flex flex-col justify-between hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
                <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">{k.get('title', '')}</span>
                <span class="w-2 h-2 rounded-full {dot_color}"></span>
            </div>
            <div class="my-3">
                <div class="text-3xl font-black text-slate-900 tracking-tight">{k.get('value', '')}</div>
                <div class="text-xs text-slate-400 mt-0.5">{k.get('subtitle', '')}</div>
            </div>
            <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                <span class="text-slate-500">Benchmark comparison:</span>
                <span class="px-2 py-0.5 rounded font-medium border {badge_class}">{k.get('delta', '')}</span>
            </div>
        </div>
        """
        
    full_html = f"""
    {TAILWIND_CDN}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {cards_html}
    </div>
    """
    components.html(full_html, height=160)


def render_insight_box(title: str, text: str, insight_type: str = "warning") -> None:
    """Renders a callout box highlighting key analytical findings."""
    color_map = {
        "warning": ("bg-amber-50", "border-amber-400", "text-amber-900", "text-amber-800", "Warning Finding"),
        "danger": ("bg-rose-50", "border-rose-500", "text-rose-950", "text-rose-800", "Critical Vulnerability"),
        "success": ("bg-emerald-50", "border-emerald-500", "text-emerald-950", "text-emerald-800", "Positive Indicator"),
        "info": ("bg-sky-50", "border-sky-500", "text-sky-950", "text-sky-800", "Analytical Insight"),
    }
    bg, bdr, text_hdr, text_body, label = color_map.get(insight_type, color_map["info"])
    
    html_code = f"""
    {TAILWIND_CDN}
    <div class="{bg} border-l-4 {bdr} p-4 rounded-r-xl shadow-sm my-4">
        <div class="flex items-center gap-2 mb-1">
            <span class="text-xs uppercase font-extrabold tracking-wider {text_hdr}">{label}: {title}</span>
        </div>
        <p class="text-sm {text_body} leading-relaxed">{text}</p>
    </div>
    """
    components.html(html_code, height=95)


def render_section_header(title: str, subtitle: str) -> None:
    """Renders a clean styled section header inside dashboard pages."""
    html_code = f"""
    {TAILWIND_CDN}
    <div class="border-b border-slate-200 pb-3 mb-4 mt-2">
        <h2 class="text-lg font-bold text-slate-800 tracking-tight">{title}</h2>
        <p class="text-xs text-slate-500">{subtitle}</p>
    </div>
    """
    components.html(html_code, height=55)
