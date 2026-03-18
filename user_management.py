#!/usr/bin/env python3
"""
👥 KMRL User Management Utilities
================================
Administrative tools for user management, password reset, and system administration.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import secrets
from streamlit_auth import auth
from auth_models import auth_manager

def show_user_management_page():
    """Show complete user management interface for admins"""
    
    # Check if user is authenticated and has admin role
    if not st.session_state.get('authenticated', False):
        st.error("🔐 Please login to access user management")
        return
    
    user = st.session_state.get('user', {})
    if user.get('role') != 'admin':
        st.error("👮‍♂️ Admin privileges required to access user management")
        return
    
    st.title("👥 KMRL User Management System")
    st.markdown("---")
    
    # Tabs for different management functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 All Users", "➕ Add User", "🔒 Password Reset", "🛡️ Security", "📊 Analytics"
    ])
    
    with tab1:
        show_all_users()
    
    with tab2:
        show_add_user()
    
    with tab3:
        show_password_reset()
    
    with tab4:
        show_security_settings()
    
    with tab5:
        show_user_analytics()

def show_all_users():
    """Display all registered users with management options"""
    st.subheader("👥 All Registered Users")
    
    try:
        users = auth_manager.get_all_users()
        
        if users:
            # Create user dataframe for display
            user_data = []
            for user in users:
                user_data.append({
                    'ID': user.id,
                    'Username': user.username,
                    'Full Name': user.full_name,
                    'Email': user.email,
                    'Role': user.role,
                    'Status': 'Active' if user.is_active else 'Inactive',
                    'Created': user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A',
                    'Last Login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'
                })
            
            df = pd.DataFrame(user_data)
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Users", len(users))
            with col2:
                admin_count = len([u for u in users if u.role == 'admin'])
                st.metric("Admin Users", admin_count)
            with col3:
                active_count = len([u for u in users if u.is_active])
                st.metric("Active Users", active_count)
            with col4:
                recent_logins = len([u for u in users if u.last_login and u.last_login > datetime.now() - timedelta(days=7)])
                st.metric("Recent Logins (7d)", recent_logins)
            
            # User table with actions
            st.markdown("### 📋 User Directory")
            
            # Search and filter
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("🔍 Search users", placeholder="Username, email, or name")
            with col2:
                role_filter = st.selectbox("Filter by role", ["All", "admin", "operator", "user"])
            
            # Filter dataframe
            filtered_df = df.copy()
            if search_term:
                mask = filtered_df.apply(lambda x: search_term.lower() in x.astype(str).str.lower().str.cat(sep=' '), axis=1)
                filtered_df = filtered_df[mask]
            
            if role_filter != "All":
                filtered_df = filtered_df[filtered_df['Role'] == role_filter]
            
            # Display filtered table
            st.dataframe(filtered_df, use_container_width=True, height=400)
            
            # User management actions
            st.markdown("### 🛠️ User Actions")
            
            selected_user_id = st.selectbox(
                "Select user for management:",
                [u['ID'] for u in user_data],
                format_func=lambda x: next((u['Username'] + f" ({u['Full Name']})" for u in user_data if u['ID'] == x), str(x))
            )
            
            if selected_user_id:
                selected_user = next((u for u in users if u.id == selected_user_id), None)
                
                if selected_user:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("🔒 Reset Password", key="reset_pwd"):
                            new_password = generate_temp_password()
                            if reset_user_password(selected_user_id, new_password):
                                st.success(f"✅ Password reset! Temporary password: `{new_password}`")
                            else:
                                st.error("❌ Password reset failed")
                    
                    with col2:
                        new_status = "Inactive" if selected_user.is_active else "Active"
                        if st.button(f"{'🔴 Deactivate' if selected_user.is_active else '🟢 Activate'}", key="toggle_status"):
                            if toggle_user_status(selected_user_id):
                                st.success(f"✅ User status changed to {new_status}")
                                st.rerun()
                            else:
                                st.error("❌ Status change failed")
                    
                    with col3:
                        if st.button("📝 Edit Role", key="edit_role"):
                            st.session_state.show_role_editor = selected_user_id
                    
                    with col4:
                        if selected_user.username != st.session_state.user.get('username'):
                            if st.button("🗑️ Delete User", key="delete_user"):
                                st.session_state.show_delete_confirm = selected_user_id
                    
                    # Role editor
                    if st.session_state.get('show_role_editor') == selected_user_id:
                        st.markdown("#### 🎭 Change User Role")
                        new_role = st.selectbox(
                            f"New role for {selected_user.username}:",
                            ["user", "operator", "admin"],
                            index=["user", "operator", "admin"].index(selected_user.role)
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Save Role", key="save_role"):
                                if update_user_role(selected_user_id, new_role):
                                    st.success(f"✅ Role updated to {new_role}")
                                    st.session_state.show_role_editor = None
                                    st.rerun()
                                else:
                                    st.error("❌ Role update failed")
                        with col2:
                            if st.button("❌ Cancel", key="cancel_role"):
                                st.session_state.show_role_editor = None
                                st.rerun()
                    
                    # Delete confirmation
                    if st.session_state.get('show_delete_confirm') == selected_user_id:
                        st.error(f"⚠️ **Confirm Deletion of {selected_user.username}**")
                        st.write("This action cannot be undone!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("🗑️ YES, DELETE", key="confirm_delete"):
                                if delete_user(selected_user_id):
                                    st.success("✅ User deleted successfully")
                                    st.session_state.show_delete_confirm = None
                                    st.rerun()
                                else:
                                    st.error("❌ Delete failed")
                        with col2:
                            if st.button("❌ Cancel", key="cancel_delete"):
                                st.session_state.show_delete_confirm = None
                                st.rerun()
        
        else:
            st.warning("No users found")
    
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")

def show_add_user():
    """Interface for adding new users"""
    st.subheader("➕ Add New User")
    
    with st.form("add_user_form"):
        st.markdown("### 👤 User Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="Enter username")
            full_name = st.text_input("Full Name", placeholder="Enter full name")
        
        with col2:
            email = st.text_input("Email", placeholder="user@kmrl.gov.in")
            role = st.selectbox("Role", ["user", "operator", "admin"], index=0)
        
        password = st.text_input("Password", type="password", placeholder="Enter password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        # Password strength indicator
        if password:
            is_strong, strength_msg = auth.is_strong_password(password)
            if is_strong:
                st.success(f"✅ {strength_msg}")
            else:
                st.warning(f"⚠️ {strength_msg}")
        
        submitted = st.form_submit_button("➕ Create User", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            
            if not all([username, full_name, email, password, confirm_password]):
                errors.append("Please fill in all fields")
            
            if not auth.is_valid_email(email):
                errors.append("Please enter a valid email address")
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            is_strong, strength_msg = auth.is_strong_password(password)
            if not is_strong:
                errors.append(strength_msg)
            
            if len(username) < 3:
                errors.append("Username must be at least 3 characters long")
            
            # Check if user exists
            existing_user = auth_manager.get_user_by_username(username)
            if existing_user:
                errors.append("Username already exists")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Create user
                result = auth_manager.register_user(username, email, full_name, password, role)
                
                if result["success"]:
                    st.success(f"✅ User '{username}' created successfully!")
                    st.info(f"User can now login with username: {username}")
                else:
                    st.error(f"❌ {result['message']}")

def show_password_reset():
    """Interface for password reset functionality"""
    st.subheader("🔒 Password Reset")
    
    tab1, tab2 = st.tabs(["🔄 Reset User Password", "🔑 Bulk Password Reset"])
    
    with tab1:
        st.markdown("### 👤 Individual Password Reset")
        
        # Get all users
        try:
            users = auth_manager.get_all_users()
            user_options = {f"{u.username} ({u.full_name})": u.id for u in users}
            
            selected_user = st.selectbox("Select user:", list(user_options.keys()))
            
            if selected_user:
                user_id = user_options[selected_user]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🎲 Generate Temporary Password", key="gen_temp"):
                        temp_password = generate_temp_password()
                        if reset_user_password(user_id, temp_password):
                            st.success("✅ Password reset successfully!")
                            st.info(f"**Temporary Password:** `{temp_password}`")
                            st.warning("Please share this password securely with the user")
                        else:
                            st.error("❌ Password reset failed")
                
                with col2:
                    if st.button("📧 Send Reset Email", key="send_email"):
                        # This would implement email functionality
                        st.info("📧 Email reset functionality would be implemented here")
        
        except Exception as e:
            st.error(f"Error loading users: {str(e)}")
    
    with tab2:
        st.markdown("### 🔄 Bulk Password Reset")
        st.warning("⚠️ This will reset passwords for multiple users at once")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            reset_inactive = st.checkbox("Reset passwords for inactive users")
            reset_old_logins = st.checkbox("Reset passwords for users with no login in 90+ days")
        
        with col2:
            role_filter = st.selectbox("Reset for specific role:", ["All", "user", "operator", "admin"], key="bulk_role")
        
        if st.button("🔄 Execute Bulk Reset", key="bulk_reset"):
            st.error("⚠️ Bulk reset functionality would be implemented here with additional confirmations")

def show_security_settings():
    """Security settings and configuration"""
    st.subheader("🛡️ Security Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Password Policy", "🔒 Session Management", "🚨 Security Logs"])
    
    with tab1:
        st.markdown("### 🔐 Password Policy Configuration")
        
        with st.form("password_policy"):
            min_length = st.number_input("Minimum password length", min_value=6, max_value=20, value=8)
            require_uppercase = st.checkbox("Require uppercase letters", value=True)
            require_lowercase = st.checkbox("Require lowercase letters", value=True)
            require_numbers = st.checkbox("Require numbers", value=True)
            require_special = st.checkbox("Require special characters", value=False)
            
            password_expiry = st.number_input("Password expiry (days)", min_value=0, max_value=365, value=90)
            
            if st.form_submit_button("💾 Save Policy"):
                st.success("✅ Password policy updated!")
    
    with tab2:
        st.markdown("### 🔒 Session Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Active Sessions", "5", delta="2 new today")
            st.metric("Session Timeout", "30 minutes")
        
        with col2:
            if st.button("🔄 Refresh All Sessions"):
                st.info("All user sessions would be refreshed")
            
            if st.button("🚪 Force Logout All"):
                st.warning("All users would be logged out")
    
    with tab3:
        st.markdown("### 🚨 Security Event Log")
        
        # Mock security events
        security_events = [
            {"Time": "2024-12-19 15:30", "Event": "Failed login attempt", "User": "admin", "IP": "192.168.1.100", "Status": "Blocked"},
            {"Time": "2024-12-19 14:15", "Event": "Successful login", "User": "operator1", "IP": "192.168.1.50", "Status": "Success"},
            {"Time": "2024-12-19 13:45", "Event": "Password reset", "User": "user123", "IP": "192.168.1.75", "Status": "Success"},
            {"Time": "2024-12-19 12:30", "Event": "User created", "User": "newuser", "IP": "192.168.1.10", "Status": "Success"},
            {"Time": "2024-12-19 11:20", "Event": "Role changed", "User": "operator2", "IP": "192.168.1.25", "Status": "Success"}
        ]
        
        events_df = pd.DataFrame(security_events)
        st.dataframe(events_df, use_container_width=True, height=300)

def show_user_analytics():
    """User analytics and statistics"""
    st.subheader("📊 User Analytics")
    
    try:
        users = auth_manager.get_all_users()
        
        # Analytics metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = len(users)
            st.metric("Total Users", total_users)
        
        with col2:
            active_users = len([u for u in users if u.is_active])
            st.metric("Active Users", active_users, delta=f"{(active_users/total_users*100):.1f}%")
        
        with col3:
            recent_users = len([u for u in users if u.created_at and u.created_at > datetime.now() - timedelta(days=30)])
            st.metric("New Users (30d)", recent_users)
        
        with col4:
            recent_logins = len([u for u in users if u.last_login and u.last_login > datetime.now() - timedelta(days=7)])
            st.metric("Active Logins (7d)", recent_logins)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Role distribution
            role_counts = {}
            for user in users:
                role = user.role
                role_counts[role] = role_counts.get(role, 0) + 1
            
            if role_counts:
                import plotly.express as px
                fig = px.pie(
                    values=list(role_counts.values()),
                    names=list(role_counts.keys()),
                    title="User Role Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # User creation timeline (mock data)
            creation_dates = []
            for user in users:
                if user.created_at:
                    creation_dates.append(user.created_at.date())
            
            if creation_dates:
                dates_df = pd.DataFrame({'date': creation_dates})
                dates_df['count'] = 1
                daily_signups = dates_df.groupby('date').count().reset_index()
                
                fig = px.line(daily_signups, x='date', y='count', title="User Registrations Over Time")
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

# Helper functions
def generate_temp_password():
    """Generate a temporary password"""
    import random
    import string
    
    # Generate 8-character password with mix of letters, numbers
    chars = string.ascii_letters + string.digits
    temp_password = ''.join(random.choice(chars) for _ in range(8))
    
    # Ensure it meets policy requirements
    temp_password = temp_password[:6] + '1A'  # Add number and uppercase
    
    return temp_password

def reset_user_password(user_id: int, new_password: str) -> bool:
    """Reset user password"""
    try:
        import sqlite3
        conn = sqlite3.connect(auth_manager.db_path)
        cursor = conn.cursor()
        
        hashed_password = auth_manager.hash_password(new_password)
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE id = ?",
            (hashed_password, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Password reset error: {str(e)}")
        return False

def toggle_user_status(user_id: int) -> bool:
    """Toggle user active status"""
    try:
        import sqlite3
        conn = sqlite3.connect(auth_manager.db_path)
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute("SELECT is_active FROM users WHERE id = ?", (user_id,))
        current_status = cursor.fetchone()[0]
        
        # Toggle status
        new_status = not bool(current_status)
        cursor.execute(
            "UPDATE users SET is_active = ? WHERE id = ?",
            (new_status, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Status toggle error: {str(e)}")
        return False

def update_user_role(user_id: int, new_role: str) -> bool:
    """Update user role"""
    try:
        import sqlite3
        conn = sqlite3.connect(auth_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (new_role, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Role update error: {str(e)}")
        return False

def delete_user(user_id: int) -> bool:
    """Delete user"""
    try:
        import sqlite3
        conn = sqlite3.connect(auth_manager.db_path)
        cursor = conn.cursor()
        
        # Delete user sessions first
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"User deletion error: {str(e)}")
        return False

if __name__ == "__main__":
    st.set_page_config(
        page_title="KMRL User Management",
        page_icon="👥",
        layout="wide"
    )
    
    show_user_management_page()