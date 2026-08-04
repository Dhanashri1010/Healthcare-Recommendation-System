"""
Theme & CSS Injection Module
-----------------------------
Generates dynamic theme CSS driven by st.session_state["theme"] using exact color tokens.
"""

import streamlit as st

def get_theme_css(theme="dark"):
    """
    Returns the complete CSS block for dark or light theme.
    Color tokens:
    Dark theme:  bg-main: #0B1120, bg-surface: #111827, bg-card: #151E2E, border: #1F2937, text-primary: #F1F5F9, text-secondary: #94A3B8
    Light theme: bg-main: #F8FAFC, bg-surface: #FFFFFF, bg-card: #FFFFFF, border: #E2E8F0, text-primary: #0F172A, text-secondary: #64748B
    Shared accent: accent-primary: #6366F1
    """
    is_dark = (theme == "dark")

    bg_main = "#0B1120" if is_dark else "#F8FAFC"
    bg_surface = "#111827" if is_dark else "#FFFFFF"
    bg_card = "#151E2E" if is_dark else "#FFFFFF"
    border = "#1F2937" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#64748B"
    card_shadow = "0 1px 3px rgba(0,0,0,0.4)" if is_dark else "0 1px 3px rgba(0,0,0,0.08)"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    :root {{
        --bg-main: {bg_main};
        --bg-surface: {bg_surface};
        --bg-card: {bg_card};
        --border: {border};
        --text-primary: {text_primary};
        --text-secondary: {text_secondary};
        --accent-primary: #6366F1;
        --accent-success: #10B981;
        --accent-warning: #F59E0B;
        --accent-danger: #EF4444;
        --card-shadow: {card_shadow};
    }}

    html, body, [class*="st-"]:not([class*="icon"]):not([class*="Icon"]):not(button) {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }}

    /* Reset font-family for Material Icons in password inputs so they render as icons, not text */
    button[aria-label="Show password"] *,
    button[aria-label="Hide password"] *,
    button[aria-label="show password"] *,
    button[aria-label="hide password"] * {{
        font-family: 'Material Symbols Outlined', 'Material Icons', sans-serif !important;
    }}

    /* Main Container Padding & Width - Up to 1400px, tight left margin */
    .block-container {{
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}

    /* Top-Right Native Header Bar (Deploy button & Hamburger Menu) Theme Styling */
    header[data-testid="stHeader"], [data-testid="stToolbar"] {{
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        z-index: 99 !important;
    }}

    header[data-testid="stHeader"] button, [data-testid="stToolbar"] button {{
        color: var(--text-primary) !important;
    }}

    /* Main Content Background Override */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }}

    /* Sidebar Background & Full Viewport Height Flex Container */
    section[data-testid="stSidebar"] {{
        background-color: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
        min-height: 100vh !important;
    }}

    [data-testid="stSidebarUserContent"] {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        min-height: calc(100vh - 2rem) !important;
        height: 100% !important;
        padding: 20px 16px !important;
    }}

    /* Cards & Form Containers */
    .saas-card, .kpi-box, .chart-card, [data-testid="stForm"] {{
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: var(--card-shadow) !important;
        color: var(--text-primary) !important;
    }}

    /* Text & Typography */
    h1, h2, h3, h4, h5, h6, .stMarkdown, label, p, [data-testid="stMarkdownContainer"] p {{
        color: var(--text-primary) !important;
    }}

    .text-secondary, .text-muted, [data-testid="stMarkdownContainer"] .text-secondary {{
        color: var(--text-secondary) !important;
    }}

    /* Inputs, Selectboxes, Multiselects */
    input, select, textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="select"] span, div[data-baseweb="tag"] {{
        color: var(--text-primary) !important;
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
    }}

    /* Tables & DataFrames */
    div[data-testid="stDataFrame"], table {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }}

    th, td {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
    }}

    /* Expanders Styling */
    div[data-testid="stExpander"] {{
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        margin-bottom: 16px !important;
    }}

    div[data-testid="stExpander"] summary {{
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
    }}

    div[data-testid="stExpander"] summary:hover {{
        color: var(--accent-primary) !important;
    }}

    div[data-testid="stExpander"] summary p {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        display: inline !important;
    }}

    /* Tabs */
    div[data-baseweb="tab-list"] {{
        background-color: transparent !important;
        border-bottom: 1px solid var(--border) !important;
    }}

    button[data-baseweb="tab"] {{
        color: var(--text-secondary) !important;
        background-color: transparent !important;
        border: none !important;
        font-weight: 600 !important;
    }}

    button[aria-selected="true"] {{
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: var(--accent-primary) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }}

    /* Sidebar Nav Radio - Clean Breathing Room Pill Style */
    div[data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 6px !important;
        margin-top: 8px !important;
    }}

    div[data-testid="stSidebar"] div[role="radiogroup"] > label {{
        padding: 10px 14px !important;
        border-radius: 8px !important;
        margin-bottom: 4px !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        border: none !important;
    }}

    div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
        background-color: rgba(99, 102, 241, 0.08) !important;
    }}

    div[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] {{
        background-color: rgba(99, 102, 241, 0.15) !important;
    }}

    div[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] p {{
        color: var(--accent-primary) !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="false"] p {{
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }}

    /* Hide Radio Circles in Sidebar Nav */
    div[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    /* Vertical Spacing Helper */
    .section-spacer {{
        margin-top: 32px !important;
    }}
    </style>
    """
    return css

def apply_theme():
    """Injects theme CSS at the top of script driven by st.session_state['theme']."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    
    css = get_theme_css(st.session_state["theme"])
    st.markdown(css, unsafe_allow_html=True)
