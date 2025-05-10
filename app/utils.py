import PyPDF2
from datetime import datetime
import google.generativeai as genai
import streamlit as st
import os

# Disease-specific facts
DIABETES_FACTS = [
    "Type 1 diabetes is an autoimmune condition where the body attacks insulin-producing cells.",
    "Type 2 diabetes accounts for about 90% of all diabetes cases worldwide.",
    "Diabetes can affect every organ in the body, including the heart, kidneys, and eyes.",
    "Regular exercise can help control blood sugar levels in people with diabetes.",
    "Diabetes is the leading cause of kidney failure in adults.",
    "The pancreas produces insulin, which helps regulate blood sugar levels.",
    "Gestational diabetes occurs during pregnancy and usually disappears after delivery.",
    "Diabetes can be managed through diet, exercise, and medication.",
    "High blood sugar levels can damage blood vessels and nerves over time.",
    "Diabetes increases the risk of heart disease and stroke."
]

KIDNEY_FACTS = [
    "Your kidneys filter about 200 quarts of blood daily.",
    "Each kidney contains about 1 million filtering units called nephrons.",
    "Kidneys help regulate blood pressure and produce red blood cells.",
    "The kidneys remove waste and excess fluid from the body.",
    "Kidney disease often has no symptoms until it's advanced.",
    "Diabetes and high blood pressure are the leading causes of kidney disease.",
    "Healthy kidneys maintain the body's fluid and electrolyte balance.",
    "Kidneys help activate vitamin D for bone health.",
    "Kidney stones are more common in men than women.",
    "The kidneys can continue to function with as little as 15% of their capacity."
]

LIVER_FACTS = [
    "The liver is the largest internal organ in the human body.",
    "The liver can regenerate itself after injury or surgery.",
    "The liver performs over 500 vital functions.",
    "The liver produces bile, which helps digest fats.",
    "The liver stores vitamins and minerals for later use.",
    "The liver helps remove toxins from the blood.",
    "Liver disease can be caused by viruses, alcohol, and obesity.",
    "The liver helps regulate blood sugar levels.",
    "The liver produces proteins essential for blood clotting.",
    "The liver can process about one alcoholic drink per hour."
]

STROKE_FACTS = [
    "A stroke occurs every 40 seconds in the United States.",
    "Stroke is the fifth leading cause of death in the US.",
    "There are two main types of stroke: ischemic and hemorrhagic.",
    "FAST is an acronym for stroke symptoms: Face drooping, Arm weakness, Speech difficulties, Time to call emergency.",
    "High blood pressure is the leading cause of stroke.",
    "Stroke can affect people of any age, including children.",
    "Women are more likely to die from stroke than men.",
    "Stroke is a leading cause of long-term disability.",
    "Quick treatment can minimize brain damage from stroke.",
    "Regular exercise can reduce stroke risk by up to 27%."
]

def get_rotating_fact(facts_list):
    today = datetime.now().date()
    fact_index = (today.day + today.month) % len(facts_list)
    return facts_list[fact_index]

def analyze_pdf(pdf_file, disease_type):
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Prepare prompt for AI analysis
        prompt = f"""Analyze this {disease_type}-related medical report and provide a summary of key findings and recommendations. 
        Focus on {disease_type}-related information and make the response concise and in bullet points.
        
        Report content:
        {text}
        """

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing PDF: {str(e)}" 