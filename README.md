# MedNexus - Advance Disease Diagnosis with ML and AI

MedNexus is a comprehensive Advance Disease Diagonosis with ML and AI platform that uses machine learning to predict various diseases including heart disease, kidney disease, diabetes, liver disease, and stroke. The platform provides an intuitive web interface for users to input their medical data and receive predictions.

## Features

- **Multiple Disease Prediction Models**
  - Heart Disease Prediction
  - Kidney Disease Prediction
  - Diabetes Prediction
  - Liver Disease Prediction
  - Stroke Prediction

- **User-Friendly Interface**
  - Interactive web application
  - Easy-to-use input forms
  - Real-time predictions
  - Visual data representation

- **AI Assistance**
  - Smart medical data analysis
  - Personalized health insights
  - Medical terminology explanations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/uchiha_byte/MedNexus.git
cd MedNexus
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app/main.py
```

## Project Structure

```
MedNexus/
├── app/
│   ├── main.py              # Main application file
│   ├── heart_disease.py     # Heart disease prediction module
│   ├── kidney_disease.py    # Kidney disease prediction module
│   ├── diabetes.py         # Diabetes prediction module
│   ├── liver_disease.py    # Liver disease prediction module
│   └── stroke.py           # Stroke prediction module
├── models/
│   ├── heart_disease_model.pkl
│   ├── kidney_disease_model.pkl
│   ├── diabetes_model.pkl
│   ├── liver_disease_model.pkl
│   └── stroke_model.pkl
├── static/
│   └── mednexus_logo.png
├── requirements.txt
├── LICENSE
└── README.md
```

## Usage

1. Launch the application using the command above
2. Select the disease prediction module from the sidebar
3. Input the required medical parameters
4. Click "Predict" to get the prediction results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for educational and research purposes only. The predictions provided by this system should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Contact

For any questions or suggestions, please open an issue in the GitHub repository.

## Project Structure

```
Disease-Prediction-main/
├── app/                    # Main application files
│   ├── kidney_app.py      # Kidney disease prediction
│   ├── heart_app.py       # Heart disease prediction
│   ├── diabetes_app.py    # Diabetes prediction
│   ├── liver_app.py       # Liver disease prediction
│   ├── stroke_app.py      # Stroke prediction
│   ├── ai_app.py          # AI-based prediction
│   ├── main.py            # Main application file
│   ├── static/            # Static assets (JS, CSS)
│   └── templates/         # Template files
├── backend/               # Model development notebooks
│   ├── Disease Prediction using Symptoms.ipynb
│   ├── Disease Detection.ipynb
│   └── Alzheimer Detection.ipynb
├── predictors/            # Trained models and preprocessing
│   ├── *_knn.pkl         # KNN models for various diseases
│   ├── *_scaler.pkl      # Data scalers
│   └── *_encoder.pkl     # Categorical data encoders
├── datasets/              # Training datasets
│   ├── kidney.csv
│   ├── heart.csv
│   ├── diabetes.csv
│   ├── liver.csv
│   ├── stroke.csv
│   └── Training.csv
├── website/              # Web interface
│   ├── index.html        # Main landing page
│   ├── *.html            # Disease-specific pages
│   ├── js/               # JavaScript files
│   ├── css/              # Stylesheets
│   └── images/           # Image assets
└── requirements.txt      # Project dependencies
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Features by Disease

### Kidney Disease Prediction
- Input Parameters:
  - Blood Pressure
  - Blood Sugar
  - Blood Urea
  - White Blood Cells
  - Hemoglobin
  - Specific Gravity
  - Albumin
  - Red Blood Cells

### Heart Disease Prediction
- Input Parameters:
  - Age
  - Sex
  - Chest Pain Type
  - Resting Blood Pressure
  - Cholesterol
  - Fasting Blood Sugar
  - Resting ECG
  - Maximum Heart Rate
  - Exercise Induced Angina
  - ST Depression
  - Slope of ST Segment
  - Number of Major Vessels
  - Thalassemia

### Diabetes Prediction
- Input Parameters:
  - Pregnancies
  - Glucose
  - Blood Pressure
  - Skin Thickness
  - Insulin
  - BMI
  - Diabetes Pedigree Function
  - Age

### Liver Disease Prediction
- Input Parameters:
  - Age
  - Gender
  - Total Bilirubin
  - Direct Bilirubin
  - Alkaline Phosphatase
  - Alamine Aminotransferase
  - Aspartate Aminotransferase
  - Total Proteins
  - Albumin
  - Albumin and Globulin Ratio

### Stroke Prediction
- Input Parameters:
  - Gender
  - Age
  - Hypertension
  - Heart Disease
  - Ever Married
  - Work Type
  - Residence Type
  - Average Glucose Level
  - BMI
  - Smoking Status

## Model Details

- **Algorithm**: K-Nearest Neighbors (KNN)
- **Preprocessing**: Standard Scaling and Label Encoding
- **Model Storage**: Pickle format (.pkl files)
- **Integration**: Google's Generative AI for medical advice



## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google's Generative AI for medical advice integration
- Scikit-learn for machine learning models
- Streamlit for the application framework
- All contributors and maintainers

## Contact

For any queries or suggestions, please reach out to the project maintainers.