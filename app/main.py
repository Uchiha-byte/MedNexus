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
from history_app import display as history_display
from auth.auth_pages import init_auth
import time
from datetime import datetime
import os
import base64
from auth.database import create_user, verify_user, init_db

# Initialize session state variables
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = True
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Navigation handler functions
def nav_button_click(page_name: str):
    st.session_state.current_page = page_name
    st.rerun()

def on_radio_change():
    st.session_state.current_page = st.session_state.navigation

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

# Configure page settings
st.set_page_config(
    page_title="MedNexus - AI-Powered Medical Diagnosis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
if not init_auth():
    st.stop()

# Load CSS files
def load_css():
    css_files = ['main.css', 'sidebar.css', 'loading.css']
    for css_file in css_files:
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', css_file), 'r') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"CSS file {css_file} not found. Please check if it exists in the static directory.")
            continue

# Load CSS
load_css()

# Add custom loading animation
def show_loading_animation():
    with st.spinner('Processing...'):
        time.sleep(0.5)

# Add tooltip component
def tooltip(text, help_text):
    return f'''
        <div class="tooltip">
            {text}
            <span class="tooltiptext">{help_text}</span>
        </div>
    '''

# Enhance prediction result display
def show_prediction(result, confidence=None):
    with st.container():
        st.markdown(f'''
            <div class="prediction-result">
                <h3>Prediction Result</h3>
                <p>{result}</p>
                {f"<p>Confidence: {confidence:.2f}%</p>" if confidence else ""}
            </div>
        ''', unsafe_allow_html=True)

# Add skeleton loading state
def skeleton_loader():
    st.markdown('''
        <div class="skeleton-loader">
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
        </div>
    ''', unsafe_allow_html=True)

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
    
    # User info section
    st.markdown(f'<p>👤 Welcome, {st.session_state["username"]}!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced navigation section
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Define navigation items with icons and descriptions
    nav_items = {
        "Home": {"icon": "🏠", "desc": "Dashboard Overview", "help": "View all available features and statistics"},
        "AI Assistance": {"icon": "🤖", "desc": "AI-Powered Medical Advice", "help": "Get personalized medical recommendations"},
        "Heart Disease": {"icon": "❤️", "desc": "Cardiac Health Analysis", "help": "Analyze heart disease risk factors"},
        "Kidney Disease": {"icon": "🫘", "desc": "Renal Function Assessment", "help": "Check kidney health indicators"},
        "Diabetes": {"icon": "🩸", "desc": "Blood Sugar Analysis", "help": "Evaluate diabetes risk factors"},
        "Liver Disease": {"icon": "🫀", "desc": "Liver Function Evaluation", "help": "Assess liver health parameters"},
        "Stroke": {"icon": "🧠", "desc": "Stroke Risk Assessment", "help": "Analyze stroke risk factors"},
        "History": {"icon": "📋", "desc": "Detection History", "help": "View your past detection results"}
    }
    
    # Create enhanced navigation options
    page = st.radio(
        "Navigation",
        list(nav_items.keys()),
        key="navigation",
        index=list(nav_items.keys()).index(st.session_state.current_page),
        on_change=on_radio_change,
        format_func=lambda x: f"{nav_items[x]['icon']} {x}",
        label_visibility="collapsed"
    )
    
    # Display enhanced description for selected page
    if page in nav_items:
        st.markdown(
            tooltip(
                f'<p class="nav-description">{nav_items[page]["desc"]}</p>',
                nav_items[page]["help"]
            ),
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Logout section
    st.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        # Clear all session state variables
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Reset authentication state
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.show_login = True
        st.session_state.show_signup = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area with enhanced UI
if st.session_state.current_page == "Home":
    # Show loading animation
    show_loading_animation()
    
    # Enhanced header section with centered gradient title
    title = "MEDNEXUS"
    animated_title = "".join([f'<span class="animated-letter">{letter}</span>' for letter in title])
    
    st.markdown(f"""
        <div class="main-header">
            <h1 aria-label="MEDNEXUS">{animated_title}</h1>
            <p class="subtitle" aria-label="Where Machine Learning Meets Lifesaving">Where Machine Learning Meets Lifesaving</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Add custom JavaScript to ensure animations keep running
    st.markdown("""
        <script>
            // Force hardware acceleration and prevent animation from being stopped
            document.querySelector('.heartbeat-line').style.transform = 'translateZ(0)';
            document.querySelector('.heartbeat-pulse').style.transform = 'translateZ(0)';
        </script>
    """, unsafe_allow_html=True)
    
    # Statistics Section
    st.write("### 📈 Health Insights Dashboard")
    
    # Create metrics cards with dark theme
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
    
    with col4:
        st.metric(
            label="AI Models",
            value="5+",
            delta="Specialized Models"
        )

    # Features Section
    st.write("### 🎯 Key Features")
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

    # Add bottom navigation using Streamlit components
    st.markdown("---")  # Add separator
    st.markdown("### Quick Navigation")
    
    # Create two rows of navigation buttons
    row1_cols = st.columns(4)
    row2_cols = st.columns(4)
    
    # First row of navigation buttons
    with row1_cols[0]:
        st.button("🏠 Home", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Home" else "secondary",
                 on_click=nav_button_click,
                 args=("Home",))
            
    with row1_cols[1]:
        st.button("🤖 AI Assistance", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "AI Assistance" else "secondary",
                 on_click=nav_button_click,
                 args=("AI Assistance",))
            
    with row1_cols[2]:
        st.button("❤️ Heart Disease", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Heart Disease" else "secondary",
                 on_click=nav_button_click,
                 args=("Heart Disease",))
            
    with row1_cols[3]:
        st.button("🫘 Kidney Disease", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Kidney Disease" else "secondary",
                 on_click=nav_button_click,
                 args=("Kidney Disease",))
    
    # Second row of navigation buttons
    with row2_cols[0]:
        st.button("🩸 Diabetes", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Diabetes" else "secondary",
                 on_click=nav_button_click,
                 args=("Diabetes",))
            
    with row2_cols[1]:
        st.button("🫀 Liver Disease", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Liver Disease" else "secondary",
                 on_click=nav_button_click,
                 args=("Liver Disease",))
            
    with row2_cols[2]:
        st.button("🧠 Stroke", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Stroke" else "secondary",
                 on_click=nav_button_click,
                 args=("Stroke",))
            
    with row2_cols[3]:
        st.button("📋 History", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_page == "History" else "secondary",
                 on_click=nav_button_click,
                 args=("History",))
    
    st.markdown("---")  # Add separator

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
    
    cols = st.columns(4)
    steps = [
        {"icon": "📝", "title": "Input Health Data", "description": "Enter your medical parameters and symptoms"},
        {"icon": "🤖", "title": "AI Analysis", "description": "Our advanced algorithms process your data"},
        {"icon": "📊", "title": "Predictive Analysis", "description": "Get accurate disease predictions"},
        {"icon": "💡", "title": "Personalized Advice", "description": "Receive AI-generated medical recommendations"}
    ]
    
    for col, step in zip(cols, steps):
        with col:
            st.info(f"### {step['icon']} {step['title']}\n{step['description']}")

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
    st.markdown("""
        <div class="cta-section">
            <h3>Ready to take control of your health?</h3>
            <p>Select a disease prediction module from the sidebar to get started.</p>
        </div>
    """, unsafe_allow_html=True)

# Disease prediction pages with enhanced UI
elif st.session_state.current_page == "AI Assistance":
    show_loading_animation()
    st.header("🤖 AI Medical Assistant")
    ai_display()
    ai_queries()

elif st.session_state.current_page == "Heart Disease":
    show_loading_animation()
    st.header("❤️ Heart Disease Prediction")
    heart_disease_display()

elif st.session_state.current_page == "Kidney Disease":
    show_loading_animation()
    st.header("🫘 Kidney Disease Prediction")
    kidney_disease_display()

elif st.session_state.current_page == "Diabetes":
    show_loading_animation()
    st.header("🩸 Diabetes Prediction")
    diabetes_display()

elif st.session_state.current_page == "Liver Disease":
    show_loading_animation()
    st.header("🫀 Liver Disease Prediction")
    liver_disease_display()

elif st.session_state.current_page == "Stroke":
    show_loading_animation()
    st.header("🧠 Stroke Prediction")
    stroke_display()

elif st.session_state.current_page == "History":
    show_loading_animation()
    st.header("📋 Detection History")
    history_display()

# Add error handling with user-friendly messages
def handle_error(error):
    st.error(f'''
        <div class="error-message">
            <h4>Oops! Something went wrong</h4>
            <p>{str(error)}</p>
            <p>Please try again or contact support if the problem persists.</p>
        </div>
    ''', unsafe_allow_html=True)

# Error handling wrapper
try:
    # Main application logic
    pass
except Exception as e:
    handle_error(e)

# Close main content wrapper at the end of the page
if st.session_state.current_page == "Home":
    st.markdown('</div>', unsafe_allow_html=True)

   

