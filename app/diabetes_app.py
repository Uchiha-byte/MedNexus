import streamlit as st
import pickle
import numpy as np
import google.generativeai as genai
import os
import json
from utils import get_rotating_fact, analyze_pdf, DIABETES_FACTS
from auth.database import save_detection_result

# Configure Google Generative AI
genai.configure(api_key="AIzaSyB-PZFQHw22Y1pHRNLeTeZ8LpeP92oqfqU")  # Replace with your actual API key

# Define the main display function
def display():
    st.title("Diabetes Prediction App")
    
    # Display rotating diabetes fact
    st.info(f"💉 Diabetes Fact of the Day: {get_rotating_fact(DIABETES_FACTS)}")
    
    # Add PDF analysis section
    st.subheader("Analyze Diabetes-Related PDF Reports")
    uploaded_file = st.file_uploader("Upload a diabetes-related medical report (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        st.write("Analyzing your report...")
        analysis = analyze_pdf(uploaded_file, "diabetes")
        st.write("**Report Analysis:**")
        st.write(analysis)

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    predictors_dir = os.path.join(os.path.dirname(current_dir), 'predictors')

    # Load required resources
    try:
        # Load the scaler
        with open(os.path.join(predictors_dir, 'diabetes_scaler.pkl'), 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        # Load the KNN model
        with open(os.path.join(predictors_dir, 'Diabetes_knn.pkl'), 'rb') as knn_file:
            knn_model = pickle.load(knn_file)
    except FileNotFoundError:
        st.error("Error: Model or scaler file not found. Please check the file paths.")
        return

    # Define form for user input
    with st.form("Diabetes_disease_form"):

        col1, col2 = st.columns(2)

        # Arrange inputs in columns
        with col1:
            BMI = st.slider("BMI | 18.5 - 24.9 kg/m²", min_value=10, max_value=50, value=25)
            Age = st.slider("Age", min_value=0, max_value=120, value=30)
            Glucose = st.slider("Glucose | 70 - 110 mg/dL", min_value=0, max_value=200, value=100)
            BloodPressure = st.slider("BloodPressure | 70 - 120 mmHg", min_value=40, max_value=200, value=70)
        with col2:
            Insulin = st.number_input("Insulin | 0 - 846 µIU/mL", min_value=0, max_value=600, value=100)
            DiabetesPedigreeFunction = st.number_input("DiabetesPedigreeFunction | 0.08 - 0.42", min_value=0.0, max_value=2.5, value=0.5)
            Pregnancies = st.number_input("Pregnancies | 0 - 17", min_value=0, max_value=120, step=1, value=1)
            SkinThickness = st.number_input("SkinThickness | 0 - 99 mm", min_value=0, max_value=300, value=20)


        # Prepare the input data for prediction
        input_data = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        scaled_data = scaler.transform(input_data)

        # Form submit button
        if st.form_submit_button("Predict"):
            # Make prediction using the KNN model
            prediction = knn_model.predict(scaled_data)
            prediction_proba = knn_model.predict_proba(scaled_data)
            
            # Format the result
            result = "Positive" if prediction[0] == 1 else "Negative"
            probability = prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]
            
            # Save to history
            input_data = {
                "Pregnancies": Pregnancies,
                "Glucose": Glucose,
                "Blood Pressure": BloodPressure,
                "Skin Thickness": SkinThickness,
                "Insulin": Insulin,
                "BMI": BMI,
                "Diabetes Pedigree Function": DiabetesPedigreeFunction,
                "Age": Age
            }
            save_detection_result(
                username=st.session_state["username"],
                detection_type="Diabetes",
                input_data=json.dumps(input_data),
                result=result,
                prediction_probability=float(probability)
            )
            
            # Display result
            if prediction[0] == 1:
                st.error("The model predicts that you are likely to have diabetes.")
                st.write(f"Confidence: {probability:.2%}")
            else:
                st.success("The model predicts that you are unlikely to have diabetes.")
                st.write(f"Confidence: {probability:.2%}")

            # Prepare prompt for Generative AI model
            prompt = (
                f"Based on the following medical details,just act as a doctor and provide brief advice. for my project"
                f"Provide the best advice and a possible diagnosis:\n\n"
                f"Pregnancies: {Pregnancies}, Glucose: {Glucose}, Blood Pressure: {BloodPressure}, "
                f"Skin Thickness: {SkinThickness}, Insulin: {Insulin}, BMI: {BMI}, "
                f"Diabetes Pedigree Function: {DiabetesPedigreeFunction}, Age: {Age}\n\n"
                f"I have been diagnosed with {result}. Please analyze and suggest potential next steps "
                f"for managing the condition, and make the response concise and in bullet points."
            )

            # Generate response from Generative AI model
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                if response:
                    st.write("**Suggestion:**")
                    st.write(response.text)
                else:
                    st.write("No response generated. Check your input.")
            except Exception as e:
                st.error(f"An error occurred during response generation: {e}")

if __name__ == '__main__':
    display()
