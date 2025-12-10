import streamlit as st
from config import COLORS


def metric_card(label: str, value: str, icon: str = None):
    """Display a modern metric card with glassmorphism effect."""
    icon_html = f"<div style='font-size:32px; margin-bottom:12px;'>{icon}</div>" if icon else ""
    html = f"""
    <div class="metric-card" style="text-align: center;">
        {icon_html}
        <div style="font-size:14px; opacity:0.7; margin-bottom:8px;">
            {label}
        </div>
        <div style="font-size:32px; font-weight:700; background: {COLORS['gradient_1']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            {value}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_metrics_row(metrics: list):
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            metric_card(metric["label"], metric["value"], metric.get("icon"))
