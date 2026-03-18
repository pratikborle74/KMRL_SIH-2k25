#!/usr/bin/env python3
"""
🔐 KMRL Streamlit Authentication Components
==========================================
Login and signup forms for Streamlit dashboard with session management.
"""

import streamlit as st
import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import re
from auth_models import auth_manager

# API Configuration
API_BASE_URL = "http://localhost:8001"

class StreamlitAuth:
    """Streamlit authentication handler"""
    
    def __init__(self):
        self.api_base = API_BASE_URL
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'access_token' not in st.session_state:
            st.session_state.access_token = None
        if 'login_error' not in st.session_state:
            st.session_state.login_error = None
        if 'signup_error' not in st.session_state:
            st.session_state.signup_error = None
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_strong_password(self, password: str) -> tuple[bool, str]:
        """Check password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Password is strong"
    
    def login_user(self, username: str, password: str) -> bool:
        """Login user via direct authentication (fallback if API not available)"""
        try:
            # Try API first
            response = requests.post(
                f"{self.api_base}/login",
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.authenticated = True
                st.session_state.user = data["user"]
                st.session_state.access_token = data["access_token"]
                st.session_state.login_error = None
                return True
            else:
                error_data = response.json()
                st.session_state.login_error = error_data.get("detail", "Login failed")
                return False
                
        except requests.exceptions.RequestException:
            # Fallback to direct authentication
            user = auth_manager.authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_active": user.is_active
                }
                st.session_state.access_token = "direct_auth"
                st.session_state.login_error = None
                return True
            else:
                st.session_state.login_error = "Invalid username or password"
                return False
    
    def register_user(self, username: str, email: str, full_name: str, password: str, role: str = "user") -> bool:
        """Register new user"""
        try:
            # Try API first
            response = requests.post(
                f"{self.api_base}/register",
                json={
                    "username": username,
                    "email": email,
                    "full_name": full_name,
                    "password": password,
                    "role": role
                },
                timeout=5
            )
            
            if response.status_code == 200:
                st.session_state.signup_error = None
                return True
            else:
                error_data = response.json()
                st.session_state.signup_error = error_data.get("detail", "Registration failed")
                return False
                
        except requests.exceptions.RequestException:
            # Fallback to direct registration
            result = auth_manager.register_user(username, email, full_name, password, role)
            if result["success"]:
                st.session_state.signup_error = None
                return True
            else:
                st.session_state.signup_error = result["message"]
                return False
    
    def logout_user(self):
        """Logout user and clear session"""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.access_token = None
        st.session_state.login_error = None
        st.session_state.signup_error = None
        st.rerun()
    
    def show_login_form(self):
        """Display login form"""
        st.markdown("### 🔐 Login to KMRL Dashboard")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                if not username or not password:
                    st.error("❌ Please fill in all fields")
                else:
                    with st.spinner("🔍 Authenticating..."):
                        if self.login_user(username, password):
                            st.success("✅ Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error(f"❌ {st.session_state.login_error}")
        
        # Display login error if any
        if st.session_state.login_error:
            st.error(f"❌ {st.session_state.login_error}")
    
    def show_signup_form(self):
        """Display signup form"""
        st.markdown("### 📝 Register for KMRL Dashboard")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("👤 Username", placeholder="Choose a username")
                email = st.text_input("📧 Email", placeholder="your.email@example.com")
            
            with col2:
                full_name = st.text_input("👨‍💼 Full Name", placeholder="Your full name")
                role = st.selectbox("🎭 Role", ["user", "operator"], index=0)
            
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            # Password strength indicator
            if password:
                is_strong, strength_msg = self.is_strong_password(password)
                if is_strong:
                    st.success(f"✅ {strength_msg}")
                else:
                    st.warning(f"⚠️ {strength_msg}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                signup_button = st.form_submit_button("📝 Sign Up", use_container_width=True)
            
            if signup_button:
                # Validation
                errors = []
                
                if not all([username, email, full_name, password, confirm_password]):
                    errors.append("Please fill in all fields")
                
                if not self.is_valid_email(email):
                    errors.append("Please enter a valid email address")
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                is_strong, strength_msg = self.is_strong_password(password)
                if not is_strong:
                    errors.append(strength_msg)
                
                if len(username) < 3:
                    errors.append("Username must be at least 3 characters long")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    with st.spinner("📝 Creating account..."):
                        if self.register_user(username, email, full_name, password, role):
                            st.success("✅ Account created successfully! Please login.")
                            st.balloons()
                            # Switch to login form
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error(f"❌ {st.session_state.signup_error}")
        
        # Display signup error if any
        if st.session_state.signup_error:
            st.error(f"❌ {st.session_state.signup_error}")
    
    def show_auth_page(self):
        """Show authentication page with login/signup toggle"""
        # Initialize toggle state
        if 'show_signup' not in st.session_state:
            st.session_state.show_signup = False
        
        # Header
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>🚆 KMRL Fleet Optimization Dashboard</h1>
            <p style='font-size: 1.2rem; color: #666;'>Secure Access Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Toggle between login and signup
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Tab-like buttons
            tab1, tab2 = st.columns(2)
            with tab1:
                if st.button("🔐 Login", use_container_width=True, 
                           type="primary" if not st.session_state.show_signup else "secondary"):
                    st.session_state.show_signup = False
                    st.rerun()
            with tab2:
                if st.button("📝 Sign Up", use_container_width=True,
                           type="primary" if st.session_state.show_signup else "secondary"):
                    st.session_state.show_signup = True
                    st.rerun()
        
        st.markdown("---")
        
        # Show appropriate form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.show_signup:
                self.show_signup_form()
            else:
                self.show_login_form()
        
        # Footer with default credentials info
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin-top: 2rem;'>
            <h4>🔧 Default Admin Credentials</h4>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> admin123</p>
            <p><em>Please change these credentials after first login!</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def show_user_info(self):
        """Show current user information in sidebar"""
        if st.session_state.authenticated and st.session_state.user:
            user = st.session_state.user
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 👤 User Information")
            
            # User details
            st.sidebar.markdown(f"**👤 Name:** {user['full_name']}")
            st.sidebar.markdown(f"**🆔 Username:** {user['username']}")
            st.sidebar.markdown(f"**📧 Email:** {user['email']}")
            
            # Role badge
            role_colors = {
                'admin': '🔴',
                'operator': '🟡', 
                'user': '🔵'
            }
            role_icon = role_colors.get(user['role'], '⚪')
            st.sidebar.markdown(f"**🎭 Role:** {role_icon} {user['role'].title()}")
            
            # Logout button
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                self.logout_user()
    
    def require_auth(self):
        """Require authentication - call this at the start of protected pages"""
        if not st.session_state.authenticated:
            st.stop()
            return False
        return True
    
    def require_role(self, required_role: str):
        """Require specific role"""
        if not st.session_state.authenticated:
            return False
        
        user_role = st.session_state.user.get('role', 'user')
        
        # Admin can access everything
        if user_role == 'admin':
            return True
        
        # Check specific role
        return user_role == required_role

# Global auth instance
auth = StreamlitAuth()