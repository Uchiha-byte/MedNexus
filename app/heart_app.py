import streamlit as st
import pickle
import numpy as np
import google.generativeai as genai
import os
import PyPDF2
import random
from datetime import datetime
import json
from utils import get_rotating_fact, analyze_pdf, HEART_FACTS
from auth.database import save_detection_result

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyB-PZFQHw22Y1pHRNLeTeZ8LpeP92oqfqU")  # Replace with your actual API key

# Heart facts that will rotate
HEART_FACTS = [
    "The heart beats about 100,000 times every day.",
    "Your heart pumps about 2,000 gallons of blood every day.",
    "The heart can continue beating even when disconnected from the body.",
    "The heart begins beating at four weeks after conception.",
    "The heart is the first organ to form during development.",
    "The heart has its own electrical system.",
    "The heart can beat on its own without any input from the brain.",
    "The heart pumps blood to all parts of the body except the corneas.",
    "The heart is located slightly to the left of the center of the chest.",
    "The heart is about the size of a fist in an adult."
]

def get_rotating_fact(facts):
    # Use the current date to determine which fact to show
    today = datetime.now().date()
    fact_index = (today.day + today.month) % len(facts)
    return facts[fact_index]

def analyze_pdf(pdf_file):
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Prepare prompt for AI analysis
        prompt = f"""Analyze this heart-related medical report and provide a summary of key findings and recommendations. 
        Focus on heart-related information and make the response concise and in bullet points.
        
        Report content:
        {text}
        """

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing PDF: {str(e)}"

# Define the main display function for the Heart Disease Prediction App
def display():
    st.title("Heart Disease Prediction App")
    
    # Display rotating heart fact
    st.info(f"💓 Heart Fact of the Day: {get_rotating_fact(HEART_FACTS)}")
    
    # Add PDF analysis section
    st.subheader("Analyze Heart-Related PDF Reports")
    uploaded_file = st.file_uploader("Upload a heart-related medical report (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        st.write("Analyzing your report...")
        analysis = analyze_pdf(uploaded_file)
        st.write("**Report Analysis:**")
        st.write(analysis)
    
    st.write("Enter the details below to predict the likelihood of heart disease.")

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    predictors_dir = os.path.join(os.path.dirname(current_dir), 'predictors')

    # Load the scaler and KNN model
    try:
        with open(os.path.join(predictors_dir, 'heart_scaler.pkl'), 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        with open(os.path.join(predictors_dir, 'heart_knn.pkl'), 'rb') as knn_file:
            knn_model = pickle.load(knn_file)
    except FileNotFoundError:
        st.error("Model or scaler files not found. Please check the file paths.")
        return

    # Define form for user input
    with st.form("Heart_disease_form"):

        col1, col2 = st.columns(2)

        # Arrange inputs in columns
        with col1:
        # Input fields for heart disease prediction
            age = st.slider("Age", min_value=0, max_value=120, step=1, value=50)
            resting_bp = st.slider("Resting Blood Pressure  > 120/80 mmHg", min_value=0, max_value=300, value=120, step=1)
            cholesterol = st.slider("Cholesterol > 200 mg/dl", min_value=0, max_value=600, value=200, step=5)
            max_hr = st.slider("Max Heart Rate Achieved", min_value=0, max_value=300, value=150, step=5)
            oldpeak = st.slider("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        with col2:
            fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["Yes", "No"], index=1)
            resting_ecg = st.selectbox("Resting ECG(Electrocardiogram | 60 - 100 bpm)", options=["Normal", "ST(ST Segment)", "LHV(Left Ventricular Hypertrophy )"], index=0)
            sex = st.selectbox("Sex", options=["Male", "Female"], index=0)
            chest_pain_type = st.selectbox("Chest Pain Type", options=["ATA(Atypical Angina)", "NAP(Non-Anginal pain)", "ASY(Asymptomatic)", "TA(Typical Angina)"], index=0)
            exercise_angina = st.selectbox("Exercise Induced Angina", options=["Yes", "No"], index=1)
            st_slope = st.selectbox("ST Segment Slope", options=["Flat", "Up", "Down"], index=0)


        # Map categorical inputs to numerical values
        sex = 0 if sex == "Male" else 1
        chest_pain_type = {"ATA(Atypical Angina)": 0, "NAP(Non-Anginal pain)": 1, "ASY(Asymptomatic)": 2, "TA(Typical Angina)": 3}[chest_pain_type]
        fasting_bs = 1 if fasting_bs == "Yes" else 0
        resting_ecg = {"Normal": 0, "ST(ST Segment)": 1, "LHV(Left Ventricular Hypertrophy )": 2}[resting_ecg]
        exercise_angina = 1 if exercise_angina == "Yes" else 0
        st_slope = {"Flat": 0, "Up": 1, "Down": 2}[st_slope]

        # Prepare the input data for prediction
        input_data = np.array([[age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, 
                                resting_ecg, max_hr, exercise_angina, oldpeak, st_slope]])
        
        # Scale the input data
        scaled_data = scaler.transform(input_data)

        # Prediction button
        if st.form_submit_button("Predict"):
            # KNN prediction
            knn_prediction = knn_model.predict(scaled_data)
            knn_result = "Heart Disease" if knn_prediction[0] == 1 else "No Heart Disease"
            st.write(f"KNN Model Prediction: {knn_result}")

            # Prepare prompt for Generative AI model
            prompt = (
                f"Based on the following medical details,just act as a doctor and provide brief advice. for my project"
                f"Provide the best advice and a possible diagnosis:\n\n"
                f"Age: {age}, Sex: {'Male' if sex == 0 else 'Female'}, Chest Pain Type: {chest_pain_type}, "
                f"Resting Blood Pressure: {resting_bp}, Cholesterol: {cholesterol}, "
                f"Fasting Blood Sugar > 120 mg/dl: {'Yes' if fasting_bs == 1 else 'No'}, "
                f"Resting ECG: {resting_ecg}, Max Heart Rate Achieved: {max_hr}, "
                f"Exercise Induced Angina: {'Yes' if exercise_angina == 1 else 'No'}, Oldpeak: {oldpeak}, "
                f"ST Slope: {st_slope}\n\n"
                f"I have been diagnosed with {knn_result}. Please analyze and suggest potential next steps "
                f"for managing the condition, and make the response concise and in bullet points."
            )

            # Generate response from Generative AI model
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                if response:
                    st.write("**Medical Advice:**")
                    st.write(response.text)
                else:
                    st.write("No response generated. Check your input.")
            except Exception as e:
                st.error(f"An error occurred during AI response generation: {e}")

            # Make prediction
            prediction = knn_model.predict(scaled_data)
            prediction_proba = knn_model.predict_proba(scaled_data)
            
            # Format the result
            result = "Positive" if prediction[0] == 1 else "Negative"
            probability = prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]
            
            # Save to history
            input_data = {
                "Age": age,
                "Sex": sex,
                "Chest Pain Type": chest_pain_type,
                "Resting Blood Pressure": resting_bp,
                "Cholesterol": cholesterol,
                "Fasting Blood Sugar": fasting_bs,
                "Resting ECG": resting_ecg,
                "Max Heart Rate": max_hr,
                "Exercise Induced Angina": exercise_angina,
                "ST Depression": oldpeak,
                "ST Slope": st_slope,
                "Number of Major Vessels": 0,  # Assuming default value
                "Thalassemia": 0  # Assuming default value
            }
            save_detection_result(
                username=st.session_state["username"],
                detection_type="Heart Disease",
                input_data=json.dumps(input_data),
                result=result,
                prediction_probability=float(probability)
            )
            
            # Display result
            if prediction[0] == 1:
                st.error("The model predicts that you are likely to have heart disease.")
                st.write(f"Confidence: {probability:.2%}")
            else:
                st.success("The model predicts that you are unlikely to have heart disease.")
                st.write(f"Confidence: {probability:.2%}")

if __name__ == '__main__':
    display()
