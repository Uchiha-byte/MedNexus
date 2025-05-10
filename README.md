# MED NEXUS
# Multi-Disease Prediction System

A comprehensive machine learning-based system for predicting various diseases using medical parameters and symptoms. This project includes both a Streamlit-based application and a web interface for disease prediction.

## Features

- **Multiple Disease Prediction Models**
  - Kidney Disease Prediction
  - Heart Disease Prediction
  - Diabetes Prediction
  - Liver Disease Prediction
  - Stroke Prediction
  - AI-based General Disease Prediction

- **Dual Interface**
  - Streamlit-based application for quick predictions
  - Web interface for a more comprehensive user experience

- **Advanced Features**
  - Integration with Google's Generative AI for medical advice
  - Real-time prediction results
  - Detailed medical parameter analysis
  - User-friendly input forms

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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/uchiha_byte/MedNexus -main.git
cd Disease-Prediction-main
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Streamlit Application

1. Navigate to the app directory:
```bash
cd app
```

2. Run the Streamlit app:
```bash
streamlit run main.py
```

3. Access the application through your web browser at `http://localhost:8501`

### Web Interface

1. Navigate to the website directory:
```bash
cd website
```

2. Open `index.html` in your web browser to access the web interface.

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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google's Generative AI for medical advice integration
- Scikit-learn for machine learning models
- Streamlit for the application framework
- All contributors and maintainers


