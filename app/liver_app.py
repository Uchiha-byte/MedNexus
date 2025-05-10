import streamlit as st
import pickle
import numpy as np
import google.generativeai as genai
import os
from utils import get_rotating_fact, analyze_pdf, LIVER_FACTS

# Configure Google Generative AI
genai.configure(api_key="AIzaSyB-PZFQHw22Y1pHRNLeTeZ8LpeP92oqfqU")  # Replace with your actual API key

# Define the main display function
def display():
    st.title("Liver Disease Prediction App")
    
    # Display rotating liver fact
    st.info(f"🫁 Liver Fact of the Day: {get_rotating_fact(LIVER_FACTS)}")
    
    # Add PDF analysis section
    st.subheader("Analyze Liver-Related PDF Reports")
    uploaded_file = st.file_uploader("Upload a liver-related medical report (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        st.write("Analyzing your report...")
        analysis = analyze_pdf(uploaded_file, "liver")
        st.write("**Report Analysis:**")
        st.write(analysis)

    st.write("Enter the medical test values below to predict the likelihood of liver disease.")

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    predictors_dir = os.path.join(os.path.dirname(current_dir), 'predictors')

    # Load the scaler and KNN model
    try:
        with open(os.path.join(predictors_dir, 'liver_scaler.pkl'), 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        with open(os.path.join(predictors_dir, 'liver_knn.pkl'), 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("Model or scaler files not found. Please check the file paths.")
        return

    # Define form for user input
    with st.form('Liver_disease_prediction'):

        col1, col2 = st.columns(2)

        # Arrange inputs in columns
        with col1:
        # Input fields with default values
            total_bilirubin = st.number_input("Total Bilirubin | 0.0 - 10.0 mg/dL", min_value=0.0, max_value=10.0, format="%.2f", value=1.0)
            direct_bilirubin = st.number_input("Direct Bilirubin | 0.0 - 5.0 mg/dL", min_value=0.0, max_value=5.0, format="%.2f", value=0.3)
            alkaline_phosphatase = st.number_input("Alkaline Phosphatase | 0 - 2000 U/L", min_value=0, max_value=2000, format="%d", value=100)
        with col2:
            alanine_aminotransferase = st.number_input("Alamine Aminotransferase (Sgpt) | 0 - 1000 U/L", min_value=0, max_value=1000, format="%d", value=20)
            total_proteins = st.number_input("Total Proteins | 0.0 - 10.0 g/dL", min_value=0.0, max_value=10.0, format="%.2f", value=6.8)
            albumin = st.number_input("Albumin | 0.0 - 5.0 g/dL", min_value=0.0, max_value=5.0, format="%.2f", value=3.5)
            albumin_globulin_ratio = st.number_input("Albumin-Globulin Ratio | 0.0 - 5.0", min_value=0.0, max_value=5.0, format="%.2f", value=1.1)

        # Prediction button
        if st.form_submit_button("Predict"):
            # Prepare feature array for prediction
            features = np.array([[total_bilirubin, direct_bilirubin, alkaline_phosphatase,
                                  alanine_aminotransferase, total_proteins, albumin,
                                  albumin_globulin_ratio]])

            # Scale the input features
            features_scaled = scaler.transform(features)

            # Make prediction using KNN model
            prediction = model.predict(features_scaled)
            result = "Positive for Liver Disease" if prediction[0] == 1 else "Negative for Liver Disease"
            st.write("KNN Model Prediction:", result)

            # Generate advice using Gemini Generative AI
            prompt = (
                f"Based on the following liver function test results,just act as a doctor and provide brief advice. for my project"
                f"Suggest potential next steps:\n\n"
                f"Total Bilirubin: {total_bilirubin}, Direct Bilirubin: {direct_bilirubin}, Alkaline Phosphatase: {alkaline_phosphatase}, "
                f"Alamine Aminotransferase (Sgpt): {alanine_aminotransferase}, Total Proteins: {total_proteins}, "
                f"Albumin: {albumin}, Albumin-Globulin Ratio: {albumin_globulin_ratio}\n\n"
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
