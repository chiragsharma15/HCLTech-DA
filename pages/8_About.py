"""
Screen UI-08: About & System Architecture
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-13
"""

import streamlit as st
from src.ui import render_header, render_section_header, render_navbar

st.set_page_config(page_title="About & Architecture | NovaTech", page_icon="ℹ️", layout="wide")

def main():
    render_navbar("About")
    render_header(
        title="About: Employee Attrition Analysis Platform",
        subtitle="MCA 2nd Year Capstone Data Analytics Project | ABES Engineering College",
        badge="System Architecture"
    )
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_section_header("Academic & Project Specifications", "Official university submission record details")
        st.markdown(r"""
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <table style="width: 100%; font-size: 0.9rem; line-height: 2;">
                    <tr><td style="color: #64748B; width: 35%;"><b>Project Title:</b></td><td style="color: #1E293B;"><b>Employee Attrition Analysis</b></td></tr>
                    <tr><td style="color: #64748B;"><b>Project ID:</b></td><td style="color: #1E293B;">EAA-2025</td></tr>
                    <tr><td style="color: #64748B;"><b>Student Author:</b></td><td style="color: #1E293B;"><b>Chirag Sharma</b> (Roll No: <code>2500320140042</code>)</td></tr>
                    <tr><td style="color: #64748B;"><b>Faculty Mentor:</b></td><td style="color: #1E293B;"><b>Mrs. Kalpna Dwivedi</b></td></tr>
                    <tr><td style="color: #64748B;"><b>Institution:</b></td><td style="color: #1E293B;">ABES Engineering College, Ghaziabad</td></tr>
                    <tr><td style="color: #64748B;"><b>Degree Program:</b></td><td style="color: #1E293B;">MCA 2nd Year (Data Analytics Specialization)</td></tr>
                    <tr><td style="color: #64748B;"><b>Target Organization:</b></td><td style="color: #1E293B;">NovaTech Solutions Pvt. Ltd., Noida (500 IT Staff)</td></tr>
                    <tr><td style="color: #64748B;"><b>Lifecycle Progress:</b></td><td style="color: #10B981; font-weight: bold;">Step 15 of 18 (Build, Test & Fix)</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        render_section_header("Technology Stack Ecosystem", "Production libraries and frameworks utilized in the solution")
        st.markdown(r"""
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
                <span style="background-color: #1B3A5C; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">Python 3.12</span>
                <span style="background-color: #FF4B4B; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">Streamlit 1.38.0</span>
                <span style="background-color: #003B57; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">SQLite 3</span>
                <span style="background-color: #3F4F75; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">Plotly 5.22.0</span>
                <span style="background-color: #38BDF8; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">Tailwind CSS 3.4</span>
                <span style="background-color: #0A9EDC; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">pytest 8.2.2</span>
                <span style="background-color: #150458; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">pandas 2.2.2</span>
                <span style="background-color: #013243; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">SciPy 1.13.1</span>
            </div>
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; font-size: 0.85rem; color: #475569;">
                <b>Layered Monolithic Architecture:</b><br>
                Embedded SQLite data layer queries cached via <code>@st.cache_data</code> into pure-Python analytical routines, rendered via Plotly SVG vectors and Tailwind layout containers.
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    # ── Section 2: Viva Examination Quick Reference Card ──
    render_section_header("Academic Viva Defense Reference", "Curated technical questions and empirical analytical findings")
    
    with st.expander("🎓 Expand Viva Defense FAQ & Key Takeaways", expanded=True):
        st.markdown(r"""
            1. **Why is this an EDA project rather than an ML prediction model?**  
               *Per the approved BRD scope (Section 6.2), EDA explains why employees voluntarily left using verifiable empirical facts, giving HR leaders actionable levers immediately without black-box ML drift.*
            
            2. **What are the top three statistically verified attrition drivers?**  
               - **Chronic Overtime:** Staff with mandatory overtime face 29.8% turnover vs. 18.2% for non-overtime staff ($\chi^2 = 18.42, p < 0.001$).  
               - **Early-Tenure Vulnerability:** Leavers with $< 2.0$ years of tenure suffer 23.7% turnover vs. 16.5% for staff with $\geq 5$ years tenure.  
               - **Compensation Inequity:** Staff in the Entry salary band (<₹25,000) experience 30.0% turnover vs. 11.0% in Leadership (>₹100,000).  
            
            3. **How does the system ensure data privacy?**  
               *The application enforces a strict No-PII policy (BRL-06). All 1,250 records were generated synthetically using Faker's `en_IN` locale with random seed 42. No real personal employee data exists anywhere.*
        """)

if __name__ == "__main__":
    main()
