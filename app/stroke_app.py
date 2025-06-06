import streamlit as st
import pickle
import numpy as np
import google.generativeai as genai
import os
import json
from utils import get_rotating_fact, analyze_pdf, STROKE_FACTS
from auth.database import save_detection_result

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyB-PZFQHw22Y1pHRNLeTeZ8LpeP92oqfqU")  # Replace with your actual API key

def display():
    st.title("Stroke Prediction App")
    
    # Display rotating stroke fact
    st.info(f"🧠 Stroke Fact of the Day: {get_rotating_fact(STROKE_FACTS)}")
    
    # Add PDF analysis section
    st.subheader("Analyze Stroke-Related PDF Reports")
    uploaded_file = st.file_uploader("Upload a stroke-related medical report (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        st.write("Analyzing your report...")
        analysis = analyze_pdf(uploaded_file, "stroke")
        st.write("**Report Analysis:**")
        st.write(analysis)

    st.write("Enter the following information to predict the likelihood of stroke.")

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    predictors_dir = os.path.join(os.path.dirname(current_dir), 'predictors')

    # Load the pre-fitted encoder, scaler, and KNN model
    try:
        with open(os.path.join(predictors_dir, 'stroke_encoder.pkl'), 'rb') as encoder_file:
            encoder = pickle.load(encoder_file)

        with open(os.path.join(predictors_dir, 'stroke_scaler.pkl'), 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        with open(os.path.join(predictors_dir, 'stroke_knn.pkl'), 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("Model or scaler files not found. Please check the file paths.")
        return

    # Define the form for user input
    with st.form("Stroke disease prediction"):
        # Divide the layout into two columns
        col1, col2 = st.columns(2)

        # Arrange inputs in columns
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
            ever_married = st.selectbox("Ever Married", ["No", "Yes"], index=0)
            work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"], index=0)
            residence_type = st.selectbox("Residence Type", ["Rural", "Urban"], index=0)
            smoking_status = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"], index=0)

        with col2:
            age = st.slider("Age", 0, 100, 25)
            hypertension = st.selectbox("Hypertension (0 = No, 1 = Yes)", [0, 1], index=0)
            heart_disease = st.selectbox("Heart Disease (0 = No, 1 = Yes)", [0, 1], index=0)
            avg_glucose_level = st.number_input("Average Glucose Level | 0.0 - 200.0 mg/dL", min_value=0.0, value=85.0)
            bmi = st.number_input("BMI | 18.5 - 24.9 kg/m²", min_value=0.0, value=24.0)


        # Prepare input data
        categorical_data = [[gender, ever_married, work_type, residence_type, smoking_status]]
        numerical_data = np.array([[age, hypertension, heart_disease, avg_glucose_level, bmi]])

        # Encode categorical data using the pre-fitted encoder
        encoded_data = encoder.transform(categorical_data)

        # Concatenate encoded and numerical data for scaling
        input_data = np.concatenate([encoded_data, numerical_data], axis=1)

        # Scale the combined data
        scaled_data = scaler.transform(input_data)

        # Perform prediction
        if st.form_submit_button("Predict"):
            prediction = model.predict(scaled_data)
            prediction_proba = model.predict_proba(scaled_data)
            
            # Format the result
            result = "High Risk" if prediction[0] == 1 else "Low Risk"
            probability = prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]
            
            # Save to history
            input_data = {
                "Age": age,
                "Gender": gender,
                "Hypertension": hypertension,
                "Heart Disease": heart_disease,
                "Ever Married": ever_married,
                "Work Type": work_type,
                "Residence Type": residence_type,
                "Average Glucose Level": avg_glucose_level,
                "BMI": bmi,
                "Smoking Status": smoking_status
            }
            save_detection_result(
                username=st.session_state["username"],
                detection_type="Stroke Risk",
                input_data=json.dumps(input_data),
                result=result,
                prediction_probability=float(probability)
            )
            
            # Display result
            if prediction[0] == 1:
                st.error("The model predicts that you are at high risk of stroke.")
                st.write(f"Confidence: {probability:.2%}")
            else:
                st.success("The model predicts that you are at low risk of stroke.")
                st.write(f"Confidence: {probability:.2%}")

            # Generate advice using Gemini Generative AI
            prompt = (
                f"Based on the following health data,just act as a doctor and provide brief advice. for my project"
                f"Suggest possible preventive actions and next steps:\n\n"
                f"Gender: {gender}, Ever Married: {ever_married}, Work Type: {work_type}, Residence Type: {residence_type}, "
                f"Smoking Status: {smoking_status}, Age: {age}, Hypertension: {hypertension}, "
                f"Heart Disease: {heart_disease}, Average Glucose Level: {avg_glucose_level}, BMI: {bmi}\n\n"
                f"The prediction indicates: {result}. Please analyze and give concise, actionable health advice."
            )

            # Generate response from Gemini AI model
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                if response:
                    st.write("**Health Advice:**")
                    st.write(response.text)
                else:
                    st.write("No response generated. Check your input.")
            except Exception as e:
                st.error(f"An error occurred during AI response generation: {e}")

if __name__ == '__main__':
    display()
