"""
KPI Cards Component Module
---------------------------
Renders polished SaaS KPI cards with subtle border, letter-spaced secondary headers, and accent values.
"""

import streamlit as st

def render_kpi_box(title, value, sub=""):
    """Renders a single polished KPI card."""
    return f"""
    <div class="kpi-box" style="
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        box-shadow: var(--card-shadow);
    ">
        <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-secondary);">{title}</div>
        <div style="font-size: 1.8rem; font-weight: 800; margin-top: 6px; color: var(--accent-primary);">{value}</div>
        {f'<div style="font-size: 0.75rem; margin-top: 4px; color: var(--text-secondary);">{sub}</div>' if sub else ''}
    </div>
    """

def render_dashboard_kpis():
    """Renders 6 KPI cards across 2 rows of 3."""
    row1_kpis = [
        {"title": "PREDICTION ACCURACY", "value": "100.0%", "sub": "Logistic Regression ML Model"},
        {"title": "TOTAL DISEASES", "value": "41", "sub": "Diagnostic Profiles"},
        {"title": "TOTAL SYMPTOMS", "value": "132", "sub": "Binary Feature Flags"}
    ]
    
    row2_kpis = [
        {"title": "DRUG REVIEWS", "value": "161,297", "sub": "Analyzed Patient Feedback"},
        {"title": "RECOMMENDATION SCORE", "value": "98.5%", "sub": "TF-IDF Cosine Match"},
        {"title": "TOTAL MEDICINES", "value": "8,423", "sub": "Indexed Drug Profiles"}
    ]

    # Row 1 (3 Cards)
    cols1 = st.columns(3)
    for idx, kpi in enumerate(row1_kpis):
        with cols1[idx]:
            st.markdown(render_kpi_box(kpi['title'], kpi['value'], kpi['sub']), unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # Row 2 (3 Cards)
    cols2 = st.columns(3)
    for idx, kpi in enumerate(row2_kpis):
        with cols2[idx]:
            st.markdown(render_kpi_box(kpi['title'], kpi['value'], kpi['sub']), unsafe_allow_html=True)

# Alias for backwards compatibility
render_top_kpi_cards = render_dashboard_kpis

def render_custom_kpis(kpis_list):
    """Renders custom KPI cards array dynamically, splitting max 3 or 4 per row."""
    num_kpis = len(kpis_list)
    cols = st.columns(num_kpis)
    for idx, kpi in enumerate(kpis_list):
        with cols[idx]:
            st.markdown(render_kpi_box(kpi['title'], kpi['value'], kpi.get('sub', '')), unsafe_allow_html=True)
