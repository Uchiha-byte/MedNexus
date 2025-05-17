# MedNexus - Advanced Disease Diagnosis with ML and AI

MedNexus is a comprehensive Advance Disease Diagonosis with ML and AI platform that uses machine learning to predict various diseases including heart disease, kidney disease, diabetes, liver disease, and stroke. The platform provides an intuitive web interface for users to input their medical data and receive predictions.

MedNexus is a state-of-the-art medical diagnosis platform that leverages machine learning and artificial intelligence to provide accurate predictions for various diseases. The platform combines traditional ML models with cutting-edge AI capabilities to deliver comprehensive health insights.

## 🌟 Key Features

### 🤖 AI-Powered Diagnosis
- Advanced ML algorithms for accurate disease prediction
- Google's Generative AI (Gemini) integration for personalized health insights
- PDF medical report analysis
- Real-time predictions and recommendations

### 🏥 Disease Prediction Models
- **Heart Disease Prediction**
  - Comprehensive cardiac health analysis
  - Multiple parameter assessment
  - Risk factor evaluation

- **Kidney Disease Prediction**
  - Renal function analysis
  - Blood parameter assessment
  - Early detection capabilities

- **Diabetes Prediction**
  - Blood sugar level analysis
  - Risk factor assessment
  - Lifestyle impact evaluation

- **Liver Disease Prediction**
  - Liver function analysis
  - Enzyme level assessment
  - Comprehensive health metrics

- **Stroke Prediction**
  - Risk factor analysis
  - Lifestyle impact assessment
  - Early warning system

### 💻 User Interface
- Intuitive web application
- Interactive input forms
- Real-time predictions
- Visual data representation
- Responsive design
- Dark/Light mode support
- Modern dark-themed interface with blue-green gradients
- Responsive and intuitive web application
- Interactive input forms with improved validation
- Real-time predictions with loading animations
- Enhanced visual hierarchy and accessibility features
- Consistent styling across all components
- Professional animations and hover effects
- Dark/Light mode support with seamless transitions

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)
- Google Cloud API key (for Gemini AI features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/uchiha_byte/MedNexus.git
cd MedNexus
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file in the root directory
GOOGLE_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app/main.py
```

## 📁 Project Structure

```
MedNexus/
├── app/                    # Main application files
│   ├── main.py            # Core application logic
│   ├── heart_app.py       # Heart disease prediction
│   ├── kidney_app.py      # Kidney disease prediction
│   ├── diabetes_app.py    # Diabetes prediction
│   ├── liver_app.py       # Liver disease prediction
│   ├── stroke_app.py      # Stroke prediction
│   ├── ai_app.py          # AI integration
│   ├── auth/              # Authentication system
│   ├── static/            # Static assets
│   └── utils/             # Utility functions
├── backend/               # Model development
│   ├── Disease Prediction using Symptoms.ipynb
│   ├── Disease Detection.ipynb
│   └── Alzheimer Detection.ipynb
├── predictors/            # Trained models
│   ├── *_knn.pkl         # KNN models
│   ├── *_scaler.pkl      # Data scalers
│   └── *_encoder.pkl     # Encoders
├── datasets/              # Training data
├── static/               # Static assets
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

## 🛠️ Technology Stack

- **Frontend**: 
  - Streamlit
  - Custom CSS with modular architecture
  - Modern UI components
  - Responsive design patterns
- **Backend**: Python
- **Machine Learning**: Scikit-learn
- **AI Integration**: Google Generative AI (Gemini)
- **Data Processing**: Pandas, NumPy
- **PDF Processing**: PyPDF2
- **Authentication**: Custom implementation
- **Model Storage**: Pickle
- **Styling**: 
  - Modern CSS3
  - CSS Grid and Flexbox
  - CSS Custom Properties
  - CSS Animations and Transitions

## 📊 Model Details

### Algorithm
- K-Nearest Neighbors (KNN)
- Standard Scaling
- Label Encoding
- Cross-validation

### Performance Metrics
- Accuracy: 95%+
- Response Time: < 5 seconds
- Real-time predictions
- Continuous model updates

## 🔒 Security Features

- User authentication
- Session management
- Secure model loading
- API key protection
- Data encryption
- Input validation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and research purposes only. The predictions provided by this system should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## 📞 Contact

- Project Link: [https://github.com/uchiha_byte/MedNexus](https://github.com/uchiha_byte/MedNexus)
- For questions or suggestions, please open an issue in the GitHub repository

## 🙏 Acknowledgments

- Google's Generative AI for medical advice integration
- Scikit-learn for machine learning models
- Streamlit for the application framework
- All contributors and maintainers
- Open-source community

## 📈 Future Enhancements

- [ ] Additional disease prediction models
- [ ] Mobile application development
- [ ] Enhanced AI capabilities
- [ ] Multi-language support
- [ ] Advanced data visualization
- [ ] Integration with medical devices
- [ ] Telemedicine features
- [ ] Patient history tracking