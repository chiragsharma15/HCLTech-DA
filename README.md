# Employee Attrition Analysis (EAA-2025)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg)](https://www.sqlite.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.22.0-3F4F75.svg)](https://plotly.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4_CDN-38BDF8.svg)](https://tailwindcss.com/)
[![Tests Passing](https://img.shields.io/badge/pytest-20%20passed-10B981.svg)](https://pytest.org/)

An executive workforce retention diagnostics and exploratory data analysis (EDA) web application built for **NovaTech Solutions Pvt. Ltd.** (Noida, UP), developed as an MCA 2nd Year Data Analytics Capstone Project at **ABES Engineering College**.

---

## 📌 Executive Summary

NovaTech Solutions Pvt. Ltd., an IT services company with approximately 500 employees, suffers an annual turnover rate of **21.28%** (costing ₹2.7–5.5 crore annually in backfills and project delays). This application replaces fragmented quarterly spreadsheets with an interactive, data-driven analytical dashboard providing empirical proof of turnover drivers to guide retention policy investments.

### 🔍 Key Empirical Findings
- **Overtime Burnout:** Employees working overtime experience a **29.79%** turnover rate vs. **18.24%** for non-overtime staff ($\chi^2 = 18.42, p < 0.001$).
- **Early-Tenure Flight Risk:** Leavers with $< 2.0$ years of tenure suffer a **23.65%** turnover rate vs. **16.54%** for staff with $\geq 5$ years tenure.
- **Compensation Inequity:** The **Entry (< ₹25,000)** salary tier has a **30.00%** turnover rate, whereas **Leadership (> ₹100,000)** maintains high stability (**11.02%**).
- **Psychometric Correlation:** Low job satisfaction and poor work-life balance scores correlate strongly with departure ($r = -0.24$).

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Core Language** | Python | `3.12.x` | Business logic & data processing |
| **Web Dashboard** | Streamlit | `1.38.0` | Reactive multi-page web framework |
| **Relational Database** | SQLite 3 | Built-in | Embedded transactional & analytical storage |
| **Data Manipulation** | pandas | `2.2.2` | DataFrames, groupby & aggregations |
| **Numerical Computing**| NumPy | `1.26.4` | Array math & vector operations |
| **Inferential Statistics**| SciPy | `1.13.1` | Chi-square & Spearman rank correlations |
| **Data Visualization** | Plotly | `5.22.0` | Interactive SVG/WebGL charts |
| **UI Design System** | Tailwind CSS | `3.4 CDN` | Corporate Navy gradient styling & KPI cards |
| **Test Automation** | pytest | `8.2.2` | Automated unit, DB integrity & UI tests |

---

## 📂 Repository Layout

```text
employee-attrition-analysis/
|-- app.py                              # Main entry point & Executive Overview router
|-- requirements.txt                    # Pinned production dependencies
|-- README.md                           # Project documentation & setup instructions
|-- BUILD_PLAN.md                       # Task-by-task build roadmap
|
|-- .streamlit/
|   |-- config.toml                     # Streamlit theme (Corporate Navy #1B3A5C)
|
|-- src/
|   |-- data_loader.py                 # SQLite reader, @st.cache_data & cleaning
|   |-- analysis.py                    # KPI math, chi-square, correlations & binning
|   |-- charts.py                      # Reusable Plotly chart factory
|   |-- filters.py                     # Global sidebar filter engine with session state
|   |-- ui.py                          # Reusable Tailwind CSS component factory
|   |-- utils.py                       # Export helpers (CSV/Excel) & formatters
|   |-- generate_data.py               # Synthetic data generator (seed 42, Faker en_IN)
|   |-- validate_data.py               # Database constraint audit script
|
|-- pages/
|   |-- 1_Overview.py                  # UI-01: Headline KPI Cards & 36-Month Trend Line
|   |-- 2_Department_Analysis.py       # UI-02: Ranked Department Turnover Bar Chart
|   |-- 3_Employee_Deep_Dive.py        # UI-03: Overtime Chi2 Test, Salary Bands & Role Heatmap
|   |-- 4_Satisfaction.py              # UI-04: Psychometric Heatmap & WLB Age Matrix
|   |-- 5_Attrition_Trends.py         # UI-05: Early-Tenure Markers, Salary Hike Box Plots, YoY
|   |-- 6_Data_Explorer.py            # UI-06: Multi-Factor Risk Profiler & CSV Export
|   |-- 7_Data_Quality.py              # UI-07: Relational Schema & Anomaly Remediation Audit
|   |-- 8_About.py                     # UI-08: Academic Metadata & Viva Reference Guide
|
|-- data/
|   |-- app.db                         # Production SQLite 3 database (5 tables + view)
|   |-- employee_attrition_data.xlsx   # Master 7-sheet analytical workbook
|   |-- *.csv                          # Individual table CSV extracts
|
|-- tests/
|   |-- conftest.py                    # Shared fixtures & 10-row deterministic test dataset
|   |-- test_data.py                   # TC-T-01 to TC-T-08 (Database & Schema Integrity)
|   |-- test_analysis.py               # TC-T-09 to TC-T-16 (KPI Formulas, Statistics & Binning)
|   |-- test_app.py                    # TC-T-17 to TC-T-20 (UI Factory, Performance & Empty State)
|
|-- docs/                              # Project specification documents (Steps 01-15)
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Clone & Install
```bash
# Clone the repository
git clone https://github.com/chirag-sharma/employee-attrition-analysis.git
cd employee-attrition-analysis

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # On Windows
# source .venv/bin/activate  # On Linux/macOS

# Install pinned dependencies
pip install -r requirements.txt
```

### 3. Launch Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing

The project includes an automated test suite with **20 unit, integration, and performance tests** achieving a **100% pass rate**:

```bash
# Run full test suite with verbose output
python -m pytest tests -v
```

---

## 👤 Project Credits & Attribution

- **Student Author:** Chirag Sharma (Roll No: `2500320140042`)
- **Faculty Mentor:** Mrs. Kalpna Dwivedi
- **Institution:** ABES Engineering College, Ghaziabad
- **Course:** Master of Computer Applications (MCA 2nd Year, Data Analytics)
- **Academic Year:** 2025–2026
