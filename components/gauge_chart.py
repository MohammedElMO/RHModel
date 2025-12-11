import streamlit as st
from config import COLORS


def display_failure_percentage(probability: float):
    """
    Displays the failure probability as a centered text and percentage value,
    without using Plotly. The color changes based on the risk level.

    Args:
        probability: A float representing failure probability (0.0 - 1.0).
    """
    # Convert 0-1 float to 0-100 percentage
    failure_pct = round(probability * 100.0, 1)

    # Determine status color based on the same ranges as the old gauge
    if failure_pct < 40:
        color_code = COLORS.get('success', '#10B981')
    elif failure_pct < 70:
        color_code = COLORS.get('warning', '#F59E0B')
    else:
        color_code = COLORS.get('danger', '#EF4444')

    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px 0; border-radius: 8px;">
            <div style="font-size: 20px; color: #4B5563; margin-bottom: 5px;">
                Probabilité de défaillance (%)
            </div>
            <div style="font-size: 60px; font-weight: bold; color: {color_code}; line-height: 1;">
                {failure_pct}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
