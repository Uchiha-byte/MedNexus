import streamlit as st
import pickle
import numpy as np
import google.generativeai as genai
import os
import json
from utils import get_rotating_fact, analyze_pdf, KIDNEY_FACTS
from auth.database import save_detection_result

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyB-PZFQHw22Y1pHRNLeTeZ8LpeP92oqfqU")  # Replace with your actual API key

def display():
    st.title("Kidney Disease Prediction App")
    
    # Display rotating kidney fact
    st.info(f"🫘 Kidney Fact of the Day: {get_rotating_fact(KIDNEY_FACTS)}")
    
    # Add PDF analysis section
    st.subheader("Analyze Kidney-Related PDF Reports")
    uploaded_file = st.file_uploader("Upload a kidney-related medical report (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        st.write("Analyzing your report...")
        analysis = analyze_pdf(uploaded_file, "kidney")
        st.write("**Report Analysis:**")
        st.write(analysis)

    st.write("Enter the test values below to predict the likelihood of kidney disease.")

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    predictors_dir = os.path.join(os.path.dirname(current_dir), 'predictors')

    # Load the scaler and KNN model
    try:
        with open(os.path.join(predictors_dir, 'kidney_scaler.pkl'), 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        with open(os.path.join(predictors_dir, 'kidney_knn.pkl'), 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("Model or scaler files not found. Please check the file paths.")
        return

    # Define form for user input
    with st.form('Kidney_disease_prediction'):

        col1, col2 = st.columns(2)

        # Arrange inputs in columns
        with col1:
        # Input fields for each feature with default values
            blood_pressure = st.slider("Blood Pressure | 80 - 130 mmHg", min_value=0, max_value=200, format="%d", value=80)
            blood_sugar = st.slider("Blood Sugar | 70 - 99 mg/dl", min_value=0, max_value=300, format="%d", value=100)
            blood_urea = st.slider("Blood Urea | 7 - 20 mg/dl", min_value=0, max_value=200, format="%d", value=40)
            white_blood_cells = st.slider("White Blood Cells | 4000 - 11000 micros/µL", min_value=0, max_value=20000, format="%d", value=8000)
        with col2:
            hemoglobin = st.number_input("Hemoglobin | 13.5 - 17.5 g/dl", min_value=0.0, max_value=20.0, format="%.2f", value=13.5)
            specific_gravity = st.number_input("Specific Gravity | 1.02 - 1.03", min_value=0.0, max_value=2.0, format="%.2f", value=1.02)
            albumin = st.number_input("Albumin | 3.5 to 5.5 gm/dl", min_value=0, max_value=10, format="%d", value=3)
            red_blood_cells = st.number_input("Red Blood Cells | 3.5 to 5.5 gm/dl", min_value=0, max_value=10, format="%d", value=5)

        # Prepare feature array for prediction
        features = np.array([[blood_pressure, specific_gravity, albumin, blood_sugar,
                              blood_urea, hemoglobin, white_blood_cells, red_blood_cells]])

        # Prediction button
        if st.form_submit_button("Predict"):
            # Scale the input features
            features_scaled = scaler.transform(features)

            # Make prediction using KNN model
            prediction = model.predict(features_scaled)
            prediction_proba = model.predict_proba(features_scaled)
            
            # Format the result
            result = "Positive" if prediction[0] == 1 else "Negative"
            probability = prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]
            
            # Save to history
            input_data = {
                "Blood Pressure": blood_pressure,
                "Specific Gravity": specific_gravity,
                "Albumin": albumin,
                "Sugar": blood_sugar,
                "Red Blood Cells": red_blood_cells,
                "Pus Cell": 0,
                "Pus Cell Clumps": 0,
                "Bacteria": 0,
                "Blood Glucose Random": 0,
                "Blood Urea": blood_urea,
                "Serum Creatinine": 0,
                "Sodium": 0,
                "Potassium": 0,
                "Hemoglobin": hemoglobin,
                "Packed Cell Volume": 0,
                "White Blood Cell Count": white_blood_cells,
                "Red Blood Cell Count": red_blood_cells,
                "Hypertension": 0,
                "Diabetes Mellitus": 0,
                "Coronary Artery Disease": 0,
                "Appetite": 0,
                "Pedal Edema": 0,
                "Anemia": 0
            }
            save_detection_result(
                username=st.session_state["username"],
                detection_type="Kidney Disease",
                input_data=json.dumps(input_data),
                result=result,
                prediction_probability=float(probability)
            )
            
            # Display result
            if prediction[0] == 1:
                st.error("The model predicts that you are likely to have kidney disease.")
                st.write(f"Confidence: {probability:.2%}")
            else:
                st.success("The model predicts that you are unlikely to have kidney disease.")
                st.write(f"Confidence: {probability:.2%}")

            # Generate advice using Gemini Generative AI
            prompt = (
                f"Based on the following medical test results,just act as a doctor and provide brief advice. for my project"
                f"Suggest potential next steps:\n\n"
                f"Blood Pressure: {blood_pressure}, Specific Gravity: {specific_gravity}, Albumin: {albumin}, "
                f"Blood Sugar: {blood_sugar}, Blood Urea: {blood_urea}, Hemoglobin: {hemoglobin}, "
                f"White Blood Cells: {white_blood_cells}, Red Blood Cells: {red_blood_cells}\n\n"
                f"The patient is diagnosed as {result}. Please analyze and provide short, actionable points for managing the condition."
            )

            # Generate response from Gemini AI model
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

if __name__ == '__main__':
    display()
