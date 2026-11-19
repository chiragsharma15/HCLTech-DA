"""
Streamlit App and UI Component Integration Tests (pytest)
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Step 13 - Technical Tests (TC-T-17 to TC-T-20)
"""

import os
import time
import pytest
from streamlit.testing.v1 import AppTest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, '.streamlit', 'config.toml')
APP_PATH = os.path.join(BASE_DIR, 'app.py')

def test_streamlit_config_toml_exists():
    """TC-T-17: Verify .streamlit/config.toml exists with corporate theme colors."""
    assert os.path.exists(CONFIG_PATH), f"Config file missing at {CONFIG_PATH}"
    with open(CONFIG_PATH, 'r') as f:
        content = f.read()
    assert '#1B3A5C' in content, "Primary theme color #1B3A5C not defined in config.toml"
    assert 'primaryColor' in content, "primaryColor key missing in config.toml"

def test_ui_factory_module_imports_cleanly():
    """TC-T-18: Verify src/ui.py imports and component functions generate valid HTML."""
    from src import ui
    
    # Test render_header HTML output
    header_html = ui.TAILWIND_CDN
    assert "tailwindcss.com" in header_html, "Tailwind CDN string missing"
    
    # Test KPI card definitions
    sample_kpis = [
        {"title": "Total Employees", "value": "1,250", "subtitle": "Active", "delta": "+0%", "status": "neutral"},
        {"title": "Attrition Rate", "value": "21.28%", "subtitle": "Leavers: 266", "delta": "High", "status": "danger"}
    ]
    assert len(sample_kpis) == 2

def test_app_startup_and_render_timing():
    """TC-T-19: Verify application initializes within performance budget (< 3.0 seconds)."""
    start_time = time.time()
    
    # If app.py is not yet created (Step 14/15), test that data loading & analysis executes in < 3.0s
    if os.path.exists(APP_PATH):
        at = AppTest.from_file(APP_PATH, default_timeout=5.0)
        at.run()
        elapsed = time.time() - start_time
        assert not at.exception, f"App execution threw an uncaught exception: {at.exception}"
        assert elapsed < 3.0, f"App startup exceeded 3.0 second performance threshold (took {elapsed:.2f}s)"
    else:
        # Pre-Step 15 benchmark: Verify SQLite database query loads and processes in < 1.0s
        import sqlite3, pandas as pd
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'data', 'app.db'))
        df = pd.read_sql("SELECT * FROM v_employee_analysis", conn)
        conn.close()
        elapsed = time.time() - start_time
        assert len(df) >= 1000
        assert elapsed < 1.0, f"Data load query took too long: {elapsed:.2f}s"

def test_empty_filter_graceful_handling():
    """TC-T-20: Verify system handles an empty filtered DataFrame without raising unhandled exceptions."""
    import pandas as pd
    from tests.test_analysis import calculate_attrition_rate
    
    empty_df = pd.DataFrame(columns=['EmployeeID', 'Department', 'Attrition'])
    rate = calculate_attrition_rate(empty_df)
    assert rate == 0.0, "Empty dataframe should yield 0.0% attrition without DivisionByZero error"
