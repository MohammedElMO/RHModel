from config import COLORS


def get_custom_css():
    """Return modern CSS with glassmorphism and system theme support."""
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit defaults */
    #MainMenu, footer, header {{display: none;}}
    
    /* Global Font */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Modern Glassmorphism Cards */
    .metric-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.3);
    }}
    
    /* Modern Status Badges */
    .status-badge {{
        border-radius: 12px;
        padding: 20px 32px;
        font-size: 24px;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }}
    
    .status-safe {{
        background: {COLORS['gradient_success']};
        color: white;
    }}
    
    .status-failure {{
        background: {COLORS['gradient_danger']};
        color: white;
    }}
    
    /* Modern Buttons */
    .stButton > button {{
        background: {COLORS['gradient_1']};
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }}
    
    /* Download Button */
    .stDownloadButton > button {{
        background: {COLORS['gradient_success']};
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Radio Buttons */
    .stRadio > div {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 8px;
    }}
    
    /* Dividers */
    hr {{
        border-color: rgba(255, 255, 255, 0.1);
    }}
    
    /* Modern Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 32px;
        font-weight: 700;
        background: {COLORS['gradient_1']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* Input Fields */
    .stSelectbox, .stSlider {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: rgba(99, 102, 241, 0.6);
        background: rgba(99, 102, 241, 0.05);
    }}
    
    /* DataFrames */
    [data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
    }}
    </style>
    """


def apply_styles():
    """Apply custom CSS to Streamlit app."""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
