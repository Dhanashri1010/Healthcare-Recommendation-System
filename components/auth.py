"""
Authentication UI Component Module
----------------------------------
Renders a centered Login & Sign Up page matching the theme of MediCare AI.
"""

import streamlit as st
from utils.db_manager import register_user, authenticate_user

def render_auth_page():
    """Renders a beautiful and centered Login & Sign Up page matching the SaaS theme."""
    # Centered layout using columns
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
        st.markdown(
            "<h2 style='text-align: center; margin-bottom: 4px; font-weight: 800; color: var(--text-primary);'>🩺 MediCare AI Platform</h2>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p class='text-secondary' style='text-align: center; margin-bottom: 24px; font-size: 0.95rem;'>Secure Patient & Clinical Analytics Portal</p>",
            unsafe_allow_html=True
        )
        
        # Tabs for Switching Modes
        auth_mode = st.tabs(["🔑 Log In", "📝 Sign Up"])
        
        with auth_mode[0]:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0px; margin-bottom: 16px; font-size: 1.25rem; font-weight: 700;'>Account Log In</h3>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                login_username = st.text_input("Username or Email", placeholder="Enter your registered username or email")
                login_password = st.text_input("Password", type="password", placeholder="Enter your account password")
                
                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                login_submit = st.form_submit_button("Log In to Portal", use_container_width=True)
                
                if login_submit:
                    if not login_username or not login_password:
                        st.error("⚠️ Please fill out all fields.")
                    else:
                        success, result = authenticate_user(login_username, login_password)
                        if success:
                            st.session_state["authenticated"] = True
                            st.session_state["username"] = result["username"]
                            st.session_state["email"] = result["email"]
                            st.success(f"✔️ Welcome back, {result['username']}! Loading dashboard...")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with auth_mode[1]:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0px; margin-bottom: 16px; font-size: 1.25rem; font-weight: 700;'>Create New Account</h3>", unsafe_allow_html=True)
            with st.form("signup_form", clear_on_submit=False):
                signup_username = st.text_input("Username", placeholder="Create a unique username")
                signup_email = st.text_input("Email Address", placeholder="Enter your email address")
                signup_password = st.text_input("Password", type="password", placeholder="Create a strong password (min 6 chars)")
                signup_confirm = st.text_input("Confirm Password", type="password", placeholder="Verify your password")
                
                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                signup_submit = st.form_submit_button("Register Account", use_container_width=True)
                
                if signup_submit:
                    if not signup_username or not signup_email or not signup_password or not signup_confirm:
                        st.error("⚠️ Please fill out all fields.")
                    elif signup_password != signup_confirm:
                        st.error("⚠️ Passwords do not match.")
                    elif len(signup_password) < 6:
                        st.error("⚠️ Password must be at least 6 characters long.")
                    elif "@" not in signup_email or "." not in signup_email:
                        st.error("⚠️ Please enter a valid email address.")
                    else:
                        success, message = register_user(signup_username, signup_email, signup_password)
                        if success:
                            st.success("🎉 Account created successfully! Please navigate to the 'Log In' tab to sign in.")
                        else:
                            st.error(f"❌ {message}")
            st.markdown("</div>", unsafe_allow_html=True)
