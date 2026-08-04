"""
Custom UI Components Module
---------------------------
Provides hero banner, recommendation result card, and glass container components with full theme awareness.
"""

import pandas as pd
import streamlit as st

def render_hero_banner():
    """Renders the top welcome banner with dynamic theme colors."""
    st.markdown("""
    <div class="hero-banner" style="
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: var(--card-shadow);
    ">
        <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-primary);">
            Enterprise AI Healthcare & Medicine Recommendation Platform
        </span>
        <h1 class="hero-banner-title" style="margin-top: 6px; margin-bottom: 8px; font-size: 2.2rem; font-weight: 800; color: var(--text-primary);">
            Personalized Healthcare Dashboard
        </h1>
        <p style="font-size: 0.95rem; margin-top: 8px; max-width: 850px; color: var(--text-secondary); line-height: 1.6;">
            High-performance AI disease prediction, content-based TF-IDF drug recommendation, metabolic BMI assessment, health risk scoring, and personalized lifestyle optimization.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_recommendation_result_card(prediction):
    """Renders the comprehensive diagnostic recommendation result card with dynamic high-contrast styling."""
    risk_color = prediction['risk_color']
    
    st.markdown(f"""
    <div class="glass-card" style="
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 6px solid {risk_color};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: var(--card-shadow);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--accent-primary);">
                    AI Diagnostic & Medication Result
                </span>
                <h2 style="font-size: 2rem; font-weight: 800; margin: 6px 0; color: var(--text-primary);">{prediction['disease']}</h2>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <span style="background: rgba(99, 102, 241, 0.15); color: var(--accent-primary); border: 1px solid var(--accent-primary); padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                        Confidence: {prediction['confidence']}%
                    </span>
                    <span style="background: {risk_color}20; color: {risk_color}; border: 1px solid {risk_color}; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                        Risk Level: {prediction['risk_level']}
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recommended Medicines Section
    st.markdown("<h3 style='color: var(--text-primary); font-weight: 800;'>💊 Top Recommended Medications (Content-Based TF-IDF Score)</h3>", unsafe_allow_html=True)
    rec_meds = prediction['recommended_medicines']
    if rec_meds:
        for idx, med in enumerate(rec_meds, 1):
            cnt_val = med.get('Useful_Review_Count')
            if pd.notnull(cnt_val) and cnt_val:
                try:
                    cnt_str = f"{int(cnt_val):,}"
                except (ValueError, TypeError):
                    cnt_str = str(cnt_val)
            else:
                cnt_str = "N/A"

            st.markdown(f"""
            <div class="glass-card" style="
                background-color: var(--bg-card);
                border: 1px solid var(--border);
                border-left: 4px solid #10B981;
                border-radius: 12px;
                padding: 18px 22px;
                margin-bottom: 14px;
                box-shadow: var(--card-shadow);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 1.1rem; color: var(--text-primary);">{idx}. {med['Drug_Name']}</strong>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 6px;">
                            ⭐ Rating: <strong style="color: var(--text-primary);">{med['Average_Rating']} / 10</strong> | 
                            👍 Useful Votes: <strong style="color: var(--text-primary);">{cnt_str}</strong> | 
                            💬 Total Reviews: <strong style="color: var(--text-primary);">{med['Total_Reviews']}</strong>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: var(--accent-primary);">{med['Recommendation_Score']}%</span>
                        <div style="font-size: 0.72rem; color: var(--text-secondary);">Match Score</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Alternative Medicines
    if prediction['alternative_medicines']:
        st.markdown("<h4 style='color: var(--text-primary); font-weight: 700;'>🔄 Alternative Medications</h4>", unsafe_allow_html=True)
        alt_str = " • ".join([f"**{m['Drug_Name']}** ({m['Average_Rating']}/10)" for m in prediction['alternative_medicines']])
        st.markdown(f"> {alt_str}")

    # Precautions, Diet & Exercise Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='color: var(--text-primary); font-weight: 700;'>🛡️ Precautions</h4>", unsafe_allow_html=True)
        for p in prediction['precautions']:
            st.markdown(f"- {p}")

    with col2:
        st.markdown("<h4 style='color: var(--text-primary); font-weight: 700;'>🥗 Healthy Diet</h4>", unsafe_allow_html=True)
        for d in prediction['diet_tips']:
            st.markdown(f"- {d}")

    with col3:
        st.markdown("<h4 style='color: var(--text-primary); font-weight: 700;'>🏃 Exercise & Recovery</h4>", unsafe_allow_html=True)
        for e in prediction['exercise_tips']:
            st.markdown(f"- {e}")
