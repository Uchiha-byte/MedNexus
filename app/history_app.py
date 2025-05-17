import streamlit as st
import json
from datetime import datetime
from auth.database import get_user_history, clear_user_history

def display():
    st.title("📋 Detection History")
    
    # Add description
    st.markdown("""
    View your past disease detection results and predictions. This history helps you track your health assessments over time.
    """)
    
    # Get user history
    history = get_user_history(st.session_state["username"])
    
    if not history:
        st.info("No detection history found. Try using some of our disease detection features!")
        return
    
    # Initialize session state for confirmation
    if 'show_confirm' not in st.session_state:
        st.session_state.show_confirm = False
    
    # Add clear history section with better layout
    st.markdown("---")  # Add a separator
    col1, col2, col3 = st.columns([6, 2, 2])
    
    # Show total records count
    with col1:
        st.write(f"Total Records: {len(history)}")
    
    # Clear history button in the last column for better alignment
    with col3:
        if not st.session_state.show_confirm:
            if st.button("🗑️ Clear History", type="secondary"):
                st.session_state.show_confirm = True
                st.rerun()
    
    # Show confirmation dialog
    if st.session_state.show_confirm:
        st.warning("⚠️ Are you sure you want to clear all history? This action cannot be undone.")
        col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
        with col2:
            if st.button("✔️ Yes, Clear", type="primary"):
                if clear_user_history(st.session_state["username"]):
                    st.session_state.show_confirm = False
                    st.success("History cleared successfully!")
                    st.rerun()
                else:
                    st.error("Failed to clear history. Please try again.")
        with col3:
            if st.button("❌ Cancel", type="secondary"):
                st.session_state.show_confirm = False
                st.rerun()
    
    st.markdown("---")  # Add a separator
    
    # Display history in an organized way
    for detection in history:
        detection_type, input_data, result, probability, timestamp = detection
        
        # Create an expander for each detection
        with st.expander(f"{detection_type} - {timestamp}", expanded=False):
            # Create three columns
            col1, col2, col3 = st.columns([2,2,1])
            
            with col1:
                st.markdown("### Input Parameters")
                try:
                    input_dict = json.loads(input_data)
                    for key, value in input_dict.items():
                        st.write(f"**{key}:** {value}")
                except:
                    st.write(input_data)
            
            with col2:
                st.markdown("### Result")
                # Add color coding based on result
                if "positive" in result.lower() or "high risk" in result.lower():
                    st.markdown(f"🔴 {result}")
                elif "negative" in result.lower() or "low risk" in result.lower():
                    st.markdown(f"🟢 {result}")
                else:
                    st.markdown(f"⚪ {result}")
            
            with col3:
                st.markdown("### Probability")
                if probability:
                    st.progress(float(probability))
                    st.write(f"{probability:.1%}")
            
            # Add timestamp in a cleaner format
            st.caption(f"Detected on: {datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y at %I:%M %p')}")

if __name__ == "__main__":
    display() 