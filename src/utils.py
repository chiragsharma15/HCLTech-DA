"""
Shared Utility Functions
Employee Attrition Analysis (EAA-2025)
Author: Chirag Sharma (Roll: 2500320140042)
Task: BUILD-05
"""

import io
import pandas as pd

def export_to_csv(df: pd.DataFrame) -> bytes:
    """Exports DataFrame to raw UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(df: pd.DataFrame) -> bytes:
    """Exports DataFrame to styled Excel (.xlsx) bytes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Filtered_Employees', index=False)
    return output.getvalue()


def format_inr(val: float) -> str:
    """Formats numeric value into Indian Rupee currency string."""
    return f"INR {val:,.0f}"


def format_pct(val: float) -> str:
    """Formats float value into standard percentage string."""
    return f"{val:.2f}%"
