import streamlit as st
from .database import create_user, verify_user, init_db
import re
import os

def validate_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def apply_auth_styles():
    """Apply common styles for authentication pages."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_file = os.path.join(current_dir, 'styles.css')
    
    # Read and apply the CSS file
    with open(css_file, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def show_mednexus_header():
    """Display the MedNexus header."""
    st.markdown("""
        <div class="mednexus-header">
            <h1 class="mednexus-title">MED NEXUS</h1>
            <p class="mednexus-subtitle">Where Machine Learning Meets Lifesaving</p>
        </div>
    """, unsafe_allow_html=True)

def show_auth_options():
    """Display the authentication options page."""
    apply_auth_styles()
    show_mednexus_header()
    
    
    st.markdown('<h2 class="welcome-title">Welcome to MedNexus</h2>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subtitle">Your AI-Powered Medical Assistant</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 Login", key="login_btn", use_container_width=True):
            st.session_state['show_login'] = True
            st.session_state['show_signup'] = False
            st.rerun()
    
    with col2:
        if st.button("📝 Sign Up", key="signup_btn", use_container_width=True):
            st.session_state['show_login'] = False
            st.session_state['show_signup'] = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_login_page():
    """Display the login page."""
    apply_auth_styles()
    show_mednexus_header()

    
    st.markdown('<h2 class="auth-title">Welcome Back!</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Please login to access your account</p>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields!")
            else:
                try:
                    if verify_user(username, password):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                except Exception as e:
                    st.error(f"An error occurred during login: {str(e)}")
    
    st.markdown('<div class="auth-link">', unsafe_allow_html=True)
    if st.button("Don't have an account? Sign up"):
        st.session_state['show_login'] = False
        st.session_state['show_signup'] = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup_page():
    """Display the signup page."""
    apply_auth_styles()
    show_mednexus_header()
    
   
    st.markdown('<h2 class="auth-title">Create Account</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Join MedNexus for personalized health insights</p>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("👤 Username")
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        submit = st.form_submit_button("Create Account")
        
        if submit:
            # Validate all fields are filled
            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all fields!")
            # Validate email format
            elif not validate_email(email):
                st.error("Please enter a valid email address!")
            # Validate password match
            elif password != confirm_password:
                st.error("Passwords do not match!")
            # Validate password length
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long!")
            else:
                try:
                    if create_user(username, email, password):
                        st.success("Account created successfully! Redirecting to login...")
                        st.session_state['show_login'] = True
                        st.session_state['show_signup'] = False
                        st.rerun()
                    else:
                        st.error("Username or email already exists!")
                except Exception as e:
                    st.error(f"An error occurred during signup: {str(e)}")
    
    st.markdown('<div class="auth-link">', unsafe_allow_html=True)
    if st.button("Already have an account? Login"):
        st.session_state['show_login'] = True
        st.session_state['show_signup'] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def init_auth():
    """Initialize authentication state."""
    try:
        # Initialize session state variables
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'show_login' not in st.session_state:
            st.session_state['show_login'] = False
        if 'show_signup' not in st.session_state:
            st.session_state['show_signup'] = False
        
        # Initialize database
        init_db()
        
        # Show appropriate page based on authentication state
        if not st.session_state['authenticated']:
            if not st.session_state['show_login'] and not st.session_state['show_signup']:
                show_auth_options()
            elif st.session_state['show_login']:
                show_login_page()
            elif st.session_state['show_signup']:
                show_signup_page()
            return False
        return True
    except Exception as e:
        st.error(f"An error occurred during authentication initialization: {str(e)}")
        return False 