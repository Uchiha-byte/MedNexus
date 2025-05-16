import streamlit as st
import numpy as np
import pandas as pd
from heart_app import display as heart_disease_display
from kidney_app import display as kidney_disease_display
from diabetes_app import display as diabetes_display
from liver_app import display as liver_disease_display
from stroke_app import display as stroke_display
from ai_app import display as ai_display
from ai_app import queries as ai_queries
from auth.auth_pages import init_auth
import time
from datetime import datetime
import os
import base64
from auth.database import create_user, verify_user, init_db

def get_base64_encoded_image():
    """Get the base64 encoded image for the logo"""
    logo_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'mednexus_logo.png'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'mednexus_logo.jpg')
    ]
    
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    return ""

# Set the page configuration
st.set_page_config(
    page_title="MED NEXUS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
if not init_auth():
    st.stop()

# Function to display logo
def display_logo(width=100):
    logo_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'mednexus_logo.png'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'mednexus_logo.jpg')
    ]
    
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            return st.image(logo_path, width=width)
    return None

# Function to load CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'sidebar.css')
    with open(css_file, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
load_css()

# Sidebar content
with st.sidebar:
    # Display circular logo area with name and slogan inside
    st.markdown('''
    <div class="sidebar-logo">
        <div class="sidebar-logo-circle"></div>
        <div class="sidebar-logo-content">
            <!-- If you want to show the logo image, uncomment the next line -->
            <!-- <img src="/static/mednexus_logo.png" alt="MedNexus Logo" /> -->
            <h1>MED NEXUS</h1>
            <p>Where Machine Learning Meets Lifesaving</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Display user info with custom styling
   
    st.write(f"Welcome, {st.session_state['username']}!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add logout button with custom styling
    st.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
    if st.button("Logout", key="logout_btn", use_container_width=True):
        # Clear all session state variables
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Reset authentication state
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['show_login'] = True
        st.session_state['show_signup'] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    # Navigation with custom styling
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Home", "AI Assistance", "Heart Disease", "Kidney Disease", "Diabetes", "Liver Disease", "Stroke"],
        format_func=lambda x: f"📊 {x}" if x == "Home" else f"🤖 {x}" if x == "AI Assistance" else f"❤️ {x}" if x == "Heart Disease" else f"🫘 {x}" if x == "Kidney Disease" else f"🩸 {x}" if x == "Diabetes" else f"🫀 {x}" if x == "Liver Disease" else f"🧠 {x}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Homepage content
if page == "Home":
    # Hero Section with centered title
    st.markdown("""
        <style>
            .main-header {
                text-align: center;
                margin: 0 auto;
                max-width: 800px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create a container for the header section
    header_container = st.container()
    with header_container:
        # Center the title and tagline
        st.markdown("""
            <div class="main-header">
                <h1 style='font-size: 4rem; font-weight: bold; color: #2196F3; margin-bottom: 0; text-shadow: 0 0 10px rgba(33, 150, 243, 0.5);'>MED NEXUS</h1>
                <p style='font-size: 1.5rem; color: #666;'>Where Machine Learning Meets Lifesaving🩺</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.write("### Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 🤖 AI-Powered Diagnosis
        Advanced ML algorithms for accurate disease prediction and personalized health insights.
        """)
    
    with col2:
        st.info("""
        ### 📊 Comprehensive Analysis
        Detailed health metrics and predictive analytics for multiple disease conditions.
        """)
    
    with col3:
        st.info("""
        ### 💡 Expert Guidance
        AI-generated medical advice and recommendations based on your health data.
        """)

    # Statistics Section
    st.write("### 📈 Health Insights Dashboard")
    
    # Create metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Accuracy Rate",
            value="95%",
            delta="Disease Prediction"
        )
    
    with col2:
        st.metric(
            label="Conditions",
            value="6+",
            delta="Diseases Covered"
        )
    
    with col3:
        st.metric(
            label="Response Time",
            value="< 5s",
            delta="Instant Analysis"
        )
    

    # Health News Section
    st.write("### 📰 Latest Health Updates")
    news_col1, news_col2 = st.columns(2)
    
    with news_col1:
        st.info("""
        ### 🧬 Breakthrough in AI Diagnostics
        Recent studies show AI systems achieving 98% accuracy in early disease detection, revolutionizing preventive healthcare.
        """)
        
        st.info("""
        ### 💊 Digital Health Revolution
        Telemedicine and AI-powered diagnostics are transforming healthcare accessibility worldwide.
        """)
    
    with news_col2:
        st.info("""
        ### 🏥 Smart Hospitals
        Integration of AI in hospitals has reduced diagnosis time by 40% and improved patient outcomes significantly.
        """)
        
        st.info("""
        ### 📱 Mobile Health Apps
        Global adoption of health monitoring apps has increased by 200% in the last year, empowering users to take control of their health.
        """)

    # How It Works Section
    st.write("### 🔍 How MED NEXUS Works")
    
    steps = [
        {"icon": "📝", "title": "Input Health Data", "description": "Enter your medical parameters and symptoms"},
        {"icon": "🤖", "title": "AI Analysis", "description": "Our advanced algorithms process your data"},
        {"icon": "📊", "title": "Predictive Analysis", "description": "Get accurate disease predictions"},
        {"icon": "💡", "title": "Personalized Advice", "description": "Receive AI-generated medical recommendations"}
    ]
    
    cols = st.columns(4)
    for col, step in zip(cols, steps):
        with col:
            st.write(f"### {step['icon']} {step['title']}")
            st.write(step['description'])

    # Health Tips Section
    st.write("### 💡 Daily Health Tips")
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.info("""
        ### 🏃‍♂️ Stay Active
        Regular exercise can reduce the risk of chronic diseases by up to 50%.
        """)
    
    with tips_col2:
        st.info("""
        ### 🥗 Balanced Diet
        A healthy diet can prevent 80% of heart disease and diabetes cases.
        """)
    
    with tips_col3:
        st.info("""
        ### 😴 Quality Sleep
        7-8 hours of sleep can improve immune function and mental health.
        """)

    # Call to Action Section
    st.write("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("### Ready to take control of your health?")
        st.write("Select a disease prediction module from the sidebar to get started.")

# Other pages
elif page == "AI Assistance":
    st.header("🤖 AI Medical Assistant")
    ai_display()
    ai_queries()

elif page == "Heart Disease":
    st.header("❤️ Heart Disease Prediction")
    heart_disease_display()

elif page == "Kidney Disease":
    st.header("🫘 Kidney Disease Prediction")
    kidney_disease_display()

elif page == "Diabetes":
    st.header("🩸 Diabetes Prediction")
    diabetes_display()

elif page == "Liver Disease":
    st.header("🫀 Liver Disease Prediction")
    liver_disease_display()

elif page == "Stroke":
    st.header("🧠 Stroke Prediction")
    stroke_display()

   

