"""
Sidebar Navigation Component Module
------------------------------------
Provides sidebar header with compact theme toggle switch (☀️/🌙) and clean vertical nav.
"""

import streamlit as st

def render_sidebar():
    """Renders logo, compact theme toggle switch, and clean vertical navigation."""
    
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"

    # Container 1: Top Branding & Toggle
    with st.sidebar.container():
        # Header Row: Logo & Compact Toggle Switch side-by-side
        col_logo, col_toggle = st.columns([3.2, 1.2])
        
        with col_logo:
            st.markdown(
                "<h3 style='margin:0; padding:4px 0 0 0; font-size: 1.15rem; font-weight: 800; color: var(--text-primary);'>🩺 MediCare AI</h3>", 
                unsafe_allow_html=True
            )
        
        with col_toggle:
            is_light = st.toggle(
                "☀️" if st.session_state["theme"] == "light" else "🌙",
                value=(st.session_state["theme"] == "light"),
                key="theme_toggle_switch"
            )
            new_theme = "light" if is_light else "dark"
            if new_theme != st.session_state["theme"]:
                st.session_state["theme"] = new_theme
                st.rerun()

        st.markdown(
            "<p style='font-size: 0.72rem; color: var(--text-secondary); margin: -4px 0 24px 0;'>Enterprise Healthcare Analytics</p>",
            unsafe_allow_html=True
        )
        st.markdown("<hr style='border: none; border-top: 1px solid var(--border); margin: 0 0 20px 0;' />", unsafe_allow_html=True)

    # Gate navigation based on authentication status
    if not st.session_state.get("authenticated", False):
        st.sidebar.info("🔒 Please log in or sign up to access the platform.")
        
        with st.sidebar.container():
            st.markdown("<hr style='border: none; border-top: 1px solid var(--border); margin: 24px 0 16px 0;' />", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size: 0.7rem; color: var(--text-secondary); text-align: center; padding-top: 4px; margin-bottom: 8px;">
                MediCare AI Platform v2.5.0<br>
                Powered by Scikit-Learn & TF-IDF
            </div>
            """, unsafe_allow_html=True)
        return None

    # Container 2: Navigation Pages (Only shown when authenticated)
    pages = [
        "🏠 Dashboard",
        "🩺 Disease Prediction",
        "⚖️ BMI Calculator",
        "🛡️ Health Risk Score",
        "🌿 Lifestyle Recommendation",
        "💊 Medicine Recommendation",
        "📊 Drug Review Analysis",
        "😊 Sentiment Analysis",
        "📈 Power BI-style Analytics",
        "📚 Disease Knowledge Base",
        "📜 Prediction History",
        "⚙ Settings"
    ]

    selected_page = st.sidebar.radio(
        "Navigation Menu",
        pages,
        label_visibility="collapsed"
    )

    # User Profile Box and Log Out Button
    with st.sidebar.container():
        st.markdown("<hr style='border: none; border-top: 1px solid var(--border); margin: 24px 0 16px 0;' />", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: 0.8rem; color: var(--text-primary); margin-bottom: 12px; line-height: 1.4;">
            👤 Logged in as:<br>
            <strong style="color: var(--accent-primary);">{st.session_state.get('username', 'User')}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Log Out", use_container_width=True, key="logout_btn"):
            st.session_state["authenticated"] = False
            st.session_state.pop("username", None)
            st.session_state.pop("email", None)
            st.rerun()

    # Container 3: Bottom Pinned Footer
    with st.sidebar.container():
        st.markdown("<hr style='border: none; border-top: 1px solid var(--border); margin: 8px 0 16px 0;' />", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.7rem; color: var(--text-secondary); text-align: center; padding-top: 4px; margin-bottom: 8px;">
            MediCare AI Platform v2.5.0<br>
            Powered by Scikit-Learn & TF-IDF
        </div>
        """, unsafe_allow_html=True)

    return selected_page
