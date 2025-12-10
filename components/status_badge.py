import streamlit as st
from config import COLORS


def status_badge(is_safe: bool):
    """Display modern status badge with gradient."""
    if is_safe:
        html = f"""
        <div class="status-badge status-safe">
            ✓ SAFE - OPERATION APPROVED
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    else:
        html = f"""
        <div class="status-badge status-failure">
            ⚠️ FAILURE RISK - MAINTENANCE NEEDED
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)


def status_with_confidence(is_safe: bool, confidence: float):
    """Display modern status with confidence score."""
    status = "SAFE" if is_safe else "FAILURE"
    icon = "✅" if is_safe else "⚠️"
    gradient = COLORS['gradient_success'] if is_safe else COLORS['gradient_danger']

    html = f"""
    <div style="background: {gradient};
                border-radius: 16px;
                padding: 32px;
                text-align: center;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);">
        <div style="font-size: 56px; font-weight: 700; color: white; margin-bottom: 16px;">
            {icon} {status}
        </div>
        <div style="font-size: 18px; color: rgba(255, 255, 255, 0.9);">
            Confidence Level: <span style="font-weight: 700; font-size: 24px;">{confidence:.1f}%</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
