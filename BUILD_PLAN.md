# BUILD_PLAN.md — Employee Attrition Analysis (EAA-2025)

> **Student:** Chirag Sharma | **Roll No:** 2500320140042 | **Course:** MCA 2nd Yr Data Analytics, ABES Engineering College  
> **Mentor:** Mrs. Kalpna Dwivedi | **Target Stack:** Python 3.12, Streamlit, SQLite, Plotly, Tailwind CSS, pytest  
> **Repository:** `D:\DA` | **Execution Phase:** Step 14 of 18 (Input for Step 15 Build Phase)

---

## 1. Project Summary & Document Register

### 10-Line Project Summary
1. **Domain & Problem:** NovaTech Solutions Pvt. Ltd., a 500-employee IT firm in Noida, experiences 18–22% annual turnover, costing ₹2.7–5.5 crore annually due to unbudgeted backfills and project delays.
2. **Current Deficiencies:** HR tracks attrition reactively via fragmented quarterly spreadsheets without centralized dashboards, statistical correlation, or multi-dimensional drill-downs.
3. **Core Solution:** A responsive, interactive web application built with Python, Streamlit, Plotly, and Tailwind CSS, backed by an embedded SQLite database (`data/app.db`).
4. **Data Foundation:** 1,250 synthetic employee records (Faker `en_IN`, seed 42) spanning 5 relational tables and a 34-column reporting view (`v_employee_analysis`).
5. **Key Business Insights:** Empirically identifies overtime burnout (29.8% vs 18.2% turnover), early-tenure flight risk (23.7% in <2 yrs), and salary band inequity (30.0% in entry tiers).
6. **Executive Dashboard:** Features 4 headline Tailwind KPI cards, 36-month trend lines, cross-department ranking bar charts, and an interactive 2D role-seniority heatmap.
7. **Psychometrics & Demographics:** Maps job/environment satisfaction correlations and work-life balance across age cohorts, providing statistical backing for HR policy interventions.
8. **Self-Service Governance:** Provides 6+ simultaneous filter dimensions with session-state persistence and one-click filtered dataset export (CSV/Excel).
9. **Verification & Quality:** Covered by 18 functional test cases (TC-F) and 20 automated pytest test cases (TC-T), achieving 100% test pass rate.
10. **Target Deployment:** Streamlit Community Cloud (free tier) with zero secrets dependency and sub-3-second load performance.

### Complete Project Deliverables Register
- **Step 01 — Project Understanding:** [`docs/01_Project_Understanding.docx`](docs/01_Project_Understanding.docx)
- **Step 02 — How Might We Statements:** [`docs/02_HMW_Statements.docx`](docs/02_HMW_Statements.docx)
- **Step 03 — Needs Analysis (BRs):** [`docs/03_Needs_Analysis.docx`](docs/03_Needs_Analysis.docx)
- **Step 04 — Requirements Traceability Matrix:** [`docs/04_Traceability_Matrix.docx`](docs/04_Traceability_Matrix.docx) | [`docs/04_Traceability_Matrix.xlsx`](docs/04_Traceability_Matrix.xlsx)
- **Step 05 — Business Requirements Document (BRD):** [`docs/05_BRD.docx`](docs/05_BRD.docx)
- **Step 07 — Technical Requirements Document (TRD):** [`docs/07_TRD.docx`](docs/07_TRD.docx)
- **Step 08 — Database Design:** [`docs/08_Database_Design.xlsx`](docs/08_Database_Design.xlsx)
- **Step 09 — ER Diagram:** [`docs/09_ER_Diagram.docx`](docs/09_ER_Diagram.docx) | [`docs/09_ER_Diagram.png`](docs/09_ER_Diagram.png)
- **Step 10 — Dataset Generation & Validation:** [`docs/10_Dataset_Validation_Report.docx`](docs/10_Dataset_Validation_Report.docx) | [`data/app.db`](data/app.db) | [`data/employee_attrition_data.xlsx`](data/employee_attrition_data.xlsx)
- **Step 11 — User Stories & Acceptance Criteria:** [`docs/11_User_Stories.docx`](docs/11_User_Stories.docx)
- **Step 12 — UI Framework Specification:** [`docs/12_UI_Framework.docx`](docs/12_UI_Framework.docx) | [`src/ui.py`](src/ui.py) | [`.streamlit/config.toml`](.streamlit/config.toml)
- **Step 13 — Test Plan & Test Suite:** [`docs/13_Test_Cases.docx`](docs/13_Test_Cases.docx) | [`tests/`](tests/)

---

## 2. Final Project Directory Structure

```text
employee-attrition-analysis/
|-- app.py                              # Main application entry point & router
|-- requirements.txt                    # Pinned production dependencies
|-- README.md                           # Comprehensive documentation & setup instructions
|-- BUILD_PLAN.md                       # Machine/Developer executable build roadmap
|
|-- .streamlit/
|   |-- config.toml                     # Streamlit theme (Corporate Navy #1B3A5C) & server settings
|
|-- src/
|   |-- __init__.py                     # Package initialization
|   |-- data_loader.py                 # SQLite reader, @st.cache_data, schema validation & cleaning
|   |-- analysis.py                    # Statistical KPI calculations, chi-square, correlations, binning
|   |-- charts.py                      # Reusable Plotly chart factory functions
|   |-- filters.py                     # Global sidebar filter engine with st.session_state
|   |-- ui.py                          # Reusable Tailwind CSS component factory
|   |-- utils.py                       # Helper functions (CSV/Excel export, formatting)
|   |-- generate_data.py               # Synthetic dataset generator (Faker en_IN, seed 42)
|   |-- validate_data.py               # Database and constraint audit script
|
|-- pages/
|   |-- 1_Overview.py                  # UI-01: Headline KPI Cards, 36-Month Trend Line, Stats Panel
|   |-- 2_Department_Analysis.py       # UI-02: Department Turnover Rankings & Volume Breakdown
|   |-- 3_Employee_Deep_Dive.py        # UI-03: Overtime Burnout, Salary Tiers, Role x Level Heatmap
|   |-- 4_Satisfaction.py              # UI-04: Psychometric Correlation Heatmap & WLB Age Matrix
|   |-- 5_Attrition_Trends.py         # UI-05: Early-Tenure Markers, Salary Hike Boxplots, YoY Trends
|   |-- 6_Data_Explorer.py            # UI-06: Multi-Factor Risk Profiler & Tabular CSV/Excel Export
|   |-- 7_Data_Quality.py              # UI-07: Transparency Audit, Schema Constraints & Anomaly Rules
|   |-- 8_About.py                     # UI-08: Academic Metadata, Architecture Diagram & Viva Review
|
|-- data/
|   |-- app.db                         # Production SQLite 3 database (5 tables + view)
|   |-- employee_attrition_data.xlsx   # Master 7-sheet analytical workbook
|   |-- departments.csv                # CSV extract: departments (6 rows)
|   |-- job_roles.csv                  # CSV extract: job_roles (12 rows)
|   |-- education_levels.csv           # CSV extract: education_levels (5 rows)
|   |-- employees.csv                  # CSV extract: clean employees fact (1,250 rows)
|   |-- satisfaction_surveys.csv       # CSV extract: satisfaction surveys (1,250 rows)
|   |-- employees_raw.csv              # CSV extract: raw records with injected test anomalies
|
|-- tests/
|   |-- __init__.py                     # Test package initialization
|   |-- conftest.py                    # Shared fixtures (tiny known dataset, db_connection)
|   |-- test_data.py                   # TC-T-01 to TC-T-08 (Database & Schema Integrity)
|   |-- test_analysis.py               # TC-T-09 to TC-T-16 (KPI Formulas, Statistics & Binning)
|   |-- test_app.py                    # TC-T-17 to TC-T-20 (UI Factory, Performance & Empty State)
|
|-- docs/                              # Formal documentation deliverables (Steps 01-14)
```

---

## 3. Step-by-Step Build Tasks (BUILD-01 to BUILD-15)

The developer or AI must execute these tasks strictly in order. Do not skip tasks.

### BUILD-01: Environment Configuration & Requirements Setup
- **Goal:** Verify and lock Python environment dependencies and Streamlit theme configuration.
- **Files Involved:** `requirements.txt`, `.streamlit/config.toml`, `.gitignore`
- **User Stories & Features:** Foundational setup supporting all user stories.
- **Exact AI Execution Prompt:**
  ```text
  Verify requirements.txt contains pinned versions: streamlit==1.38.0, pandas==2.2.2, numpy==1.26.4, scipy==1.13.1, plotly==5.22.0, Faker==25.0.0, pytest==8.2.2, openpyxl==3.1.5. Ensure .streamlit/config.toml sets primaryColor='#1B3A5C', backgroundColor='#FFFFFF', secondaryBackgroundColor='#F8FAFC', and textColor='#1E293B'. Add .gitignore for Python bytecode, virtual environments, and temporary OS files.
  ```
- **How to Check:** Run `python -c "import streamlit, pandas, plotly, scipy, openpyxl; print('All core libraries imported successfully')"`
- **Tests That Must Pass:** `tests/test_app.py::test_streamlit_config_toml_exists`

---

### BUILD-02: Data Access Layer & Cleaning Pipeline (`src/data_loader.py`)
- **Goal:** Build the cached database loader that queries `data/app.db`, validates schema constraints, and handles missing/outlier values gracefully.
- **Files Involved:** `src/data_loader.py`
- **User Stories & Features:** `US-01`, `US-02` | `F-01`, `FR-01`, `NFR-06`
- **Exact AI Execution Prompt:**
  ```text
  Create src/data_loader.py. Implement load_data() decorated with @st.cache_data(ttl=3600). Connect to data/app.db, execute 'PRAGMA foreign_keys = ON;', and load 'SELECT * FROM v_employee_analysis'. Implement validate_schema(df) checking >= 1,000 rows, zero nulls in primary columns, and valid Age/Salary ranges. Implement clean_raw_data(df) to impute missing NumCompaniesWorked with median (2.0), impute missing DistanceFromHome with role median, deduplicate on EmployeeID, and cap outlier distances at 30 km.
  ```
- **How to Check:** Run `python -c "from src.data_loader import load_data; df = load_data(); print('Loaded rows:', len(df), 'cols:', df.shape[1])"`
- **Tests That Must Pass:** `tests/test_data.py::test_database_file_exists`, `test_table_presence_and_row_counts`, `test_foreign_key_integrity`

---

### BUILD-03: Statistical & KPI Analytical Engine (`src/analysis.py`)
- **Goal:** Implement all mathematical, aggregation, binning, and inferential statistical routines.
- **Files Involved:** `src/analysis.py`
- **User Stories & Features:** `US-01` to `US-14` | `F-01` to `F-10`, `FR-05`, `FR-08`, `FR-09`, `FR-14`, `FR-16`
- **Exact AI Execution Prompt:**
  ```text
  Create src/analysis.py. Implement compute_headline_kpis(df) returning total employees, leavers, attrition rate %, and average leaver tenure. Implement get_monthly_trend(df) grouping by DateOfLeaving. Implement get_department_summary(df) returning headcount, leavers, and attrition % ranked descending. Implement calculate_overtime_stats(df) returning cohort rates and scipy.stats.chi2_contingency results. Implement get_salary_band_summary(df), get_role_level_matrix(df), compute_satisfaction_correlations(df), get_wlb_age_matrix(df), get_tenure_breakdown(df), and compare_salary_hikes(df). Ensure all division operations guard against division by zero when df is empty.
  ```
- **How to Check:** Run `python -c "from src.analysis import compute_headline_kpis; from src.data_loader import load_data; print(compute_headline_kpis(load_data()))"`
- **Tests That Must Pass:** `tests/test_analysis.py::test_kpi_overall_attrition_rate_formula`, `test_chi_square_contingency_calculation`, `test_spearman_rank_correlation`, `test_empty_filter_graceful_handling`

---

### BUILD-04: Visual Chart Factory (`src/charts.py`)
- **Goal:** Implement Plotly visual figure generators enforcing corporate Navy palette and responsive layout.
- **Files Involved:** `src/charts.py`
- **User Stories & Features:** Supporting all UI visual specifications (`UI-01` to `UI-06`).
- **Exact AI Execution Prompt:**
  ```text
  Create src/charts.py. Implement Plotly figure generators: plot_attrition_trend_line(df), plot_department_ranking_bar(df), plot_overtime_comparison_bar(df, stats_dict), plot_salary_band_bar(df), plot_role_level_heatmap(df), plot_satisfaction_correlation_heatmap(df), plot_wlb_age_heatmap(df), plot_tenure_band_bar(df), plot_salary_hike_boxplot(df), plot_yoy_department_trend(df), and plot_demographic_sunburst(df). Use clean transparent margins, custom hover tooltips, and color-code high-attrition bars in Rose-Crimson (#E11D48) and normal in Navy (#1B3A5C). Set config={'displayModeBar': False, 'responsive': True}.
  ```
- **How to Check:** Run `python -c "from src.charts import plot_department_ranking_bar; from src.data_loader import load_data; fig = plot_department_ranking_bar(load_data()); print('Chart created:', type(fig))"`
- **Tests That Must Pass:** Chart generation returns valid `plotly.graph_objects.Figure` instances without exceptions.

---

### BUILD-05: Global Sidebar Filter Engine (`src/filters.py`)
- **Goal:** Construct reactive sidebar controls with `st.session_state` persistence and reset functionality.
- **Files Involved:** `src/filters.py`
- **User Stories & Features:** `US-14` | `F-10`, `FR-12`
- **Exact AI Execution Prompt:**
  ```text
  Create src/filters.py. Implement render_sidebar_filters(df) -> pd.DataFrame. Add widgets: Department multi-select, Job Role multi-select, OverTime radio ('All', 'Yes', 'No'), Age Range slider (min_age to max_age), Gender checkboxes, and Salary Band multi-select. Bind widget keys to st.session_state. Add a 'Reset All Filters' button that clears session state filters and triggers st.rerun(). Filter the input DataFrame through a chained boolean mask. Display active filter count badge. If filtered DataFrame has 0 rows, display st.warning and return empty DataFrame gracefully.
  ```
- **How to Check:** Verify sidebar renders in Streamlit and filtered DataFrame reacts to selections.
- **Tests That Must Pass:** `tests/test_app.py::test_empty_filter_graceful_handling`

---

### BUILD-06: Main Entry Point & Executive Overview Page (`app.py` & `pages/1_Overview.py`)
- **Goal:** Build main Streamlit configuration router and the Executive Overview dashboard screen.
- **Files Involved:** `app.py`, `pages/1_Overview.py`
- **User Stories & Features:** `US-01` to `US-05` | `F-01`, `FR-01`, `FR-02`, `FR-03`, `FR-16`, `UI-01`
- **Exact AI Execution Prompt:**
  ```text
  Create app.py configuring st.set_page_config(page_title='Employee Attrition Analysis', layout='wide', page_icon='📊'). Redirect or render default landing page. In pages/1_Overview.py, import render_header, render_kpi_row, render_insight_box from src.ui; load data via src.data_loader; apply filters via src.filters. Render Tailwind header banner, 4 headline KPI cards, interactive 36-month trend line chart (src.charts), and a collapsible container displaying descriptive statistics (mean, median, std dev, Q1, Q3) for numerical columns.
  ```
- **How to Check:** Run `streamlit run app.py` and inspect browser on `http://localhost:8501`.
- **Tests That Must Pass:** `TC-F-01`, `TC-F-02`, `TC-F-06`, `TC-F-07`

---

### BUILD-07: Department Analysis Page (`pages/2_Department_Analysis.py`)
- **Goal:** Implement cross-department comparative turnover rankings, volume breakdown, and sortable metrics.
- **Files Involved:** `pages/2_Department_Analysis.py`
- **User Stories & Features:** `US-06` | `F-02`, `FR-04`, `UI-02`
- **Exact AI Execution Prompt:**
  ```text
  Create pages/2_Department_Analysis.py. Render Tailwind header banner. Load data and apply filters. Display insight callout highlighting that Sales (~26.5%) and R&D (~22.8%) exceed company average. Render horizontal ranked bar chart of department attrition %. Render side-by-side volume breakdown (active headcount vs. leaver count). Render an interactive sortable st.dataframe summarizing Department, Headcount, Leavers, Attrition Rate %, and Critical Risk Role.
  ```
- **How to Check:** Navigate to `Department Analysis` in sidebar; verify ranked bar chart and sortable table.
- **Tests That Must Pass:** `TC-F-03`, `TC-F-08`, `TC-F-09`

---

### BUILD-08: Workforce Deep-Dive Page (`pages/3_Employee_Deep_Dive.py`)
- **Goal:** Implement Overtime burnout evaluation with $\chi^2$ test, Salary Band bars, and Role $	imes$ Seniority heatmap.
- **Files Involved:** `pages/3_Employee_Deep_Dive.py`
- **User Stories & Features:** `US-07`, `US-08`, `US-09` | `F-03`, `F-04`, `F-05`, `FR-05`, `FR-06`, `FR-07`, `UI-03`
- **Exact AI Execution Prompt:**
  ```text
  Create pages/3_Employee_Deep_Dive.py. Render Tailwind header. Section 1 (Overtime): Display grouped bar comparing OverTime=Yes (29.8%) vs No (18.2%); display Chi-Square test result card (statistic, p-value < 0.001, and interpretation confirming statistical significance). Section 2 (Compensation): Display ordered bar chart of attrition across Entry, Mid-Junior, Senior, Leadership bands. Section 3 (Hierarchy): Render 2D interactive Plotly heatmap cross-tabulating 12 Job Roles by 5 Job Levels, highlighting vulnerable intersections like Laboratory Technician Level 1.
  ```
- **How to Check:** Verify Chi-Square card shows $p < 0.05$ and heatmap renders 60 cells cleanly.
- **Tests That Must Pass:** `TC-F-05`, `TC-F-10`, `TC-F-11`, `TC-F-12`

---

### BUILD-09: Psychometrics & Satisfaction Page (`pages/4_Satisfaction.py`)
- **Goal:** Implement correlation heatmap, Likert score attrition distributions, and WLB $	imes$ Age matrix.
- **Files Involved:** `pages/4_Satisfaction.py`
- **User Stories & Features:** `US-10`, `US-11` | `F-06`, `F-07`, `FR-08`, `FR-09`, `FR-14`, `UI-04`
- **Exact AI Execution Prompt:**
  ```text
  Create pages/4_Satisfaction.py. Render Tailwind header. Display correlation matrix heatmap for JobSatisfaction, EnvironmentSatisfaction, WorkLifeBalance, RelationshipSatisfaction, and Attrition. Display grouped bar chart showing attrition percentage across Likert scores 1, 2, 3, and 4 (demonstrating sharp departure drops above score 2). Render stacked heatmap/bar cross-tabulating Work-Life Balance ratings against Age Brackets (<30, 30-40, 41-50, >50), highlighting that young staff with poor WLB have peak turnover (>40%).
  ```
- **How to Check:** Verify heatmap correlation values match negative rho and WLB matrix displays age brackets.
- **Tests That Must Pass:** `TC-F-13`, `TC-F-14`

---

### BUILD-10: Tenure & Longitudinal Trends Page (`pages/5_Attrition_Trends.py`)
- **Goal:** Implement early-tenure flight risk markers, salary hike box plots, and multi-year YoY department line chart.
- **Files Involved:** `pages/5_Attrition_Trends.py`
- **User Stories & Features:** `US-12`, `US-13`, `US-16` | `F-08`, `F-09`, `F-12`, `FR-10`, `FR-11`, `FR-15`, `UI-05`
- **Exact AI Execution Prompt:**
  ```text
  Create pages/5_Attrition_Trends.py. Render Tailwind header. Section 1: Display tenure distribution bar chart highlighting '< 2 Years (Early-Tenure)' in crimson (showing 23.7% turnover vs 16.5% for tenured). Section 2: Display Plotly box plot comparing PercentSalaryHike distributions between stayers (median ~16.5%) and leavers (median ~13.8%). Section 3: Display multi-year YoY department line chart plotting annual turnover rates across calendar years 2023, 2024, 2025, and 2026.
  ```
- **How to Check:** Verify box plot renders two distinct cohorts and early-tenure bar is visually highlighted.
- **Tests That Must Pass:** `TC-F-15`, `TC-F-16`, `TC-F-17`

---

### BUILD-11: Multi-Factor Risk Profiler & Data Explorer (`pages/6_Data_Explorer.py`)
- **Goal:** Build the interactive multi-dimensional risk explorer and one-click tabular CSV/Excel download engine.
- **Files Involved:** `pages/6_Data_Explorer.py`, `src/utils.py`
- **User Stories & Features:** `US-14`, `US-15` | `F-10`, `F-11`, `FR-12`, `FR-13`, `UI-06`
- **Exact AI Execution Prompt:**
  ```text
  Create src/utils.py with export_to_csv(df) and export_to_excel(df) returning binary data. Create pages/6_Data_Explorer.py. Render Tailwind header. Allow simultaneous filtering across Age, Gender, MaritalStatus, EducationField, Distance, and OverTime. Display an active subset summary card showing matching employee count and subset attrition rate. Render Plotly Sunburst chart (Department -> Role -> OverTime -> Attrition). Display filtered records in st.dataframe. Provide 'Download Filtered Data (CSV)' and 'Download Master Excel (.xlsx)' buttons.
  ```
- **How to Check:** Filter data, click 'Download Filtered Data (CSV)', and inspect downloaded CSV in Excel/text editor.
- **Tests That Must Pass:** `TC-F-04`, `TC-F-18`

---

### BUILD-12: Data Quality & Validation Audit Page (`pages/7_Data_Quality.py`)
- **Goal:** Implement transparency audit screen showcasing schema constraints, foreign key validation, and cleaning rules.
- **Files Involved:** `pages/7_Data_Quality.py`
- **User Stories & Features:** `US-02` | `FR-01`, `NFR-08`, `UI-07`
- **Exact AI Execution Prompt:**
  ```text
  Create pages/7_Data_Quality.py. Render Tailwind header. Section 1 (Live Database Audit): Display live table counts, PK uniqueness status, and PRAGMA foreign_key_check results (showing 0 violations). Section 2 (Data Cleaning Pipeline): Display raw vs clean comparison table showcasing how injected missing values in NumCompaniesWorked (31 rows) and DistanceFromHome (25 rows) were imputed, how 3 duplicate employee rows were resolved, and how salary/commute outliers were capped. Add a button to re-run live validation audit dynamically.
  ```
- **How to Check:** Open Data Quality page; verify all 5 SQLite tables show green 'PASS' badges.
- **Tests That Must Pass:** `TC-T-01` through `TC-T-08`

---

### BUILD-13: About & Architecture Page (`pages/8_About.py`)
- **Goal:** Build academic metadata display, technology badges, system architecture diagram, and viva reference card.
- **Files Involved:** `pages/8_About.py`
- **User Stories & Features:** `US-01` | Metadata & Governance, `UI-08`
- **Exact AI Execution Prompt:**
  ```text
  Create pages/8_About.py. Render Tailwind header. Display project specification card (Title, Domain, Student: Chirag Sharma, Roll: 2500320140042, Mentor: Mrs. Kalpna Dwivedi, ABES Engineering College). Render technology stack pill badges (Python 3.12, Streamlit 1.38, SQLite, Plotly, Tailwind, pytest). Render Mermaid architecture diagram illustrating data flow (SQLite -> pandas -> SciPy -> Plotly -> Streamlit). Add collapsible viva review notes summarizing the 10 core operational questions and key statistical takeaways.
  ```
- **How to Check:** Verify student roll number, mentor name, and tech stack badges display accurately.
- **Tests That Must Pass:** Page renders cleanly with zero exceptions.

---

### BUILD-14: Full Automated Test Suite Verification & Performance Hardening
- **Goal:** Run entire pytest test suite, verify 100% pass rate, and check page-load performance budget (< 3.0s).
- **Files Involved:** `tests/test_data.py`, `tests/test_analysis.py`, `tests/test_app.py`
- **User Stories & Features:** Verification of all BRs, FRs, and NFRs.
- **Exact AI Execution Prompt:**
  ```text
  Execute 'python -m pytest tests -v'. Verify all 20 test cases pass. Ensure AppTest initializes without exceptions. Verify that full database read and view aggregation takes < 1.0 second on local machine. Fix any syntax warnings or deprecation notices.
  ```
- **How to Check:** Terminal output displays `20 passed in X.XXs` with 0 failures.
- **Tests That Must Pass:** All 20 tests in `TC-T-01` to `TC-T-20`.

---

### BUILD-15: Repository Documentation, README & Deployment Preparation
- **Goal:** Author production `README.md` with system overview, architecture diagram, setup instructions, and deployment guide.
- **Files Involved:** `README.md`
- **User Stories & Features:** Final release readiness for Streamlit Community Cloud.
- **Exact AI Execution Prompt:**
  ```text
  Create comprehensive README.md at repository root. Include: Project Title, Badge bar (Python, Streamlit, SQLite, pytest), Project Overview (NovaTech scenario), Key Features & Dashboards, System Architecture & Technology Stack, Installation & Local Execution Guide (pip install, streamlit run), Testing Guide (pytest commands), Database Schema summary, Live Cloud URL placeholder, Author & Academic Acknowledgements.
  ```
- **How to Check:** Inspect `README.md` on GitHub or markdown previewer.

---

## 4. Definition of Done (DoD)

A build task or release milestone is considered **DONE** only when all the following criteria are met:
1. **Business Requirements Fulfilled:** All 12 Business Requirements (BR-01 to BR-12) and 16 Functional Requirements are implemented in code.
2. **Automated Tests Passing:** All 20 automated pytest tests in `tests/` pass with 100% success rate (`0 failures`).
3. **Data Integrity Confirmed:** SQLite database (`data/app.db`) enforces foreign keys with zero referential integrity violations.
4. **Performance Threshold Met:** Initial application page load completes in $< 3.0$ seconds; filter interactions recalculate in $< 1.5$ seconds.
5. **Zero Uncaught Exceptions:** No runtime errors, unhandled division-by-zero crashes, or blank screen anomalies when filters yield 0 records.
6. **Code Quality Standards:** Clean modular code with docstrings, type hints, and separation of concerns (`src/` vs `pages/`).
7. **Traceability Maintained:** All RTM matrix columns (OQ, HMW, BR, Feature, DB Column, User Story, UI Screen, Test Case) are 100% populated.
8. **Documentation Complete:** Project documents (Steps 01 to 14) and root `README.md` are finalized.

---

## 5. Execution Commands Quick Reference

### Setup & Installation
```bash
# Clone repository
git clone https://github.com/<username>/employee-attrition-analysis.git
cd employee-attrition-analysis

# Create & activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate  # On Linux/macOS

# Install pinned dependencies
pip install -r requirements.txt
```

### Dataset Generation & Live Validation
```bash
# Regenerate synthetic database & extracts (deterministic seed 42)
python src/generate_data.py

# Run database integrity and constraint audit
python src/validate_data.py
```

### Run Automated Tests
```bash
# Execute entire test suite with verbose output
python -m pytest tests -v

# Run specific test modules
python -m pytest tests/test_data.py -v
python -m pytest tests/test_analysis.py -v
python -m pytest tests/test_app.py -v
```

### Launch Streamlit Web Application
```bash
# Run local multi-page development server
streamlit run app.py
```

---

## 6. Viva Examination Notes: Top 10 Questions & Short Answers

1. **Q: What is the primary business problem your application solves?**  
   *A:* It replaces fragmented, delayed quarterly HR spreadsheets with an on-demand interactive analytics dashboard, allowing NovaTech Solutions to identify attrition drivers (overtime, early tenure, low pay) and reduce annual turnover from 21.3% toward the 12–15% industry benchmark.

2. **Q: Why did you choose Streamlit, SQLite, and Plotly instead of a traditional web stack (React + Django + PostgreSQL)?**  
   *A:* Streamlit enables reactive, pure-Python data dashboards with minimal boilerplate; SQLite provides a zero-configuration, serverless relational database committed directly into the Git repository; and Plotly renders interactive, publication-quality vector charts with hover tooltips.

3. **Q: What is the significance of the $\chi^2$ (Chi-Square) test on the Overtime Deep-Dive screen?**  
   *A:* It statistically proves that the departure differential between overtime staff (29.8%) and non-overtime staff (18.2%) is statistically significant ($p < 0.001, 	ext{dof}=1$), proving that overtime is a genuine departure driver rather than random noise.

4. **Q: How did you ensure your synthetic data generation is reproducible and realistic?**  
   *A:* We locked the pseudo-random generator with `seed = 42` (NumPy and Python random), utilized Faker's `en_IN` locale for fictional Indian demographics, and passed weighted behavioral risk scores through a calibrated logistic sigmoid function ($c = 1.52$) yielding an overall attrition rate of 21.28%.

5. **Q: Why is `SalaryBand` denormalized in the `employees` table when it can be calculated from `MonthlyIncome`?**  
   *A:* Analytical denormalization. Pre-computing and indexing the 4 categorical salary tiers with a database `CHECK` constraint avoids repetitive `CASE` evaluations during high-frequency dashboard filter slicing, boosting query performance while preserving data hygiene.

6. **Q: How does `st.session_state` maintain filter context across multi-page navigation?**  
   *A:* Streamlit reruns scripts from top to bottom on user interaction and destroys local variables during page switches. By binding widget keys to `st.session_state`, active filter selections (e.g., Department='Sales') persist across page transitions without resetting.

7. **Q: What was your testing strategy across the project lifecycle?**  
   *A:* We used Behavior-Driven Development (BDD) via Given/When/Then acceptance criteria for 18 functional tests (TC-F), and Test-Driven Development (TDD) via 20 automated pytest tests (TC-T) covering schema constraints, KPI formulas on tiny controlled datasets, and UI load timing (< 3s).

8. **Q: Why did you separate `satisfaction_surveys` into a 1:1 related table instead of merging it into `employees`?**  
   *A:* Domain separation of concerns. Core employment and payroll attributes originate from master HRMS records, whereas engagement survey responses represent self-reported psychometric ratings. A 1:1 table maintains 3NF hygiene and allows future multi-wave survey expansion without altering the core schema.

9. **Q: How does your application handle edge cases such as empty filter results?**  
   *A:* All statistical aggregation and rate functions guard against `len(df) == 0` by returning `0.0%` rather than dividing by zero, while the UI displays a clean `st.warning("No employees match active filters")` callout rather than crashing with an unhandled exception.

10. **Q: What makes this project an Exploratory Data Analysis (EDA) tool rather than a Machine Learning model?**  
    *A:* Per our approved project scope (BRD Section 6.2), EDA focuses on descriptive and inferential diagnostics—explaining *why* past employees left using empirical historical facts—which HR managers and CFOs can immediately act upon, whereas predictive black-box ML models are prone to bias and require ongoing model retraining.
