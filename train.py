import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)

class MedicalModelTrainer:
    def __init__(self, dataset_name):
        """
        Initialize the trainer for a specific medical condition dataset.
        
        Args:
            dataset_name (str): Name of the dataset (heart, kidney, liver, diabetes, stroke)
        """
        self.dataset_name = dataset_name
        self.data = None
        self.X = None
        self.y = None
        self.model = None
        self.scaler = StandardScaler()
        
        # Define dataset specific configurations
        self.dataset_configs = {
            'heart': {
                'file_path': 'datasets/heart.csv',
                'target_column': 'target',
                'drop_columns': []
            },
            'kidney': {
                'file_path': 'datasets/kidney.csv',
                'target_column': 'classification',
                'drop_columns': []
            },
            'liver': {
                'file_path': 'datasets/liver.csv',
                'target_column': 'Dataset',
                'drop_columns': []
            },
            'diabetes': {
                'file_path': 'datasets/diabetes.csv',
                'target_column': 'Outcome',
                'drop_columns': []
            },
            'stroke': {
                'file_path': 'datasets/stroke.csv',
                'target_column': 'stroke',
                'drop_columns': ['id']
            }
        }

    def load_data(self):
        """Load and prepare the dataset."""
        try:
            config = self.dataset_configs[self.dataset_name]
            logging.info(f"Loading {self.dataset_name} dataset...")
            
            # Load the data
            self.data = pd.read_csv(config['file_path'])
            
            # Remove specified columns
            self.data = self.data.drop(columns=config['drop_columns'], errors='ignore')
            
            # Handle missing values
            self.data = self.handle_missing_values(self.data)
            
            # Prepare features and target
            self.y = self.data[config['target_column']]
            self.X = self.data.drop(columns=[config['target_column']])
            
            # Handle categorical variables
            self.X = self.handle_categorical_variables(self.X)
            
            logging.info(f"Dataset loaded successfully. Shape: {self.X.shape}")
            return True
            
        except Exception as e:
            logging.error(f"Error loading dataset: {str(e)}")
            return False

    def handle_missing_values(self, data):
        """Handle missing values in the dataset."""
        # For numerical columns, fill with median
        numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
        data[numerical_cols] = data[numerical_cols].fillna(data[numerical_cols].median())
        
        # For categorical columns, fill with mode
        categorical_cols = data.select_dtypes(include=['object']).columns
        data[categorical_cols] = data[categorical_cols].fillna(data[categorical_cols].mode().iloc[0])
        
        return data

    def handle_categorical_variables(self, data):
        """Convert categorical variables to numerical using one-hot encoding."""
        return pd.get_dummies(data)

    def train_model(self, test_size=0.2, random_state=42):
        """
        Train the model using Random Forest Classifier.
        
        Args:
            test_size (float): Proportion of dataset to include in the test split
            random_state (int): Random state for reproducibility
        """
        try:
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=test_size, random_state=random_state
            )
            
            # Scale the features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Initialize and train the model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=random_state
            )
            
            logging.info("Training model...")
            self.model.fit(X_train_scaled, y_train)
            
            # Make predictions and evaluate
            y_pred = self.model.predict(X_test_scaled)
            
            # Calculate and log metrics
            accuracy = accuracy_score(y_test, y_pred)
            logging.info(f"Model Accuracy: {accuracy:.4f}")
            
            # Log detailed classification report
            logging.info("\nClassification Report:")
            logging.info(classification_report(y_test, y_pred))
            
            # Save the model and scaler
            self.save_model()
            
            return True
            
        except Exception as e:
            logging.error(f"Error during training: {str(e)}")
            return False

    def save_model(self):
        """Save the trained model and scaler."""
        try:
            # Create directory if it doesn't exist
            os.makedirs('predictors', exist_ok=True)
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save model
            model_filename = f"predictors/{self.dataset_name}_model_{timestamp}.joblib"
            scaler_filename = f"predictors/{self.dataset_name}_scaler_{timestamp}.joblib"
            
            joblib.dump(self.model, model_filename)
            joblib.dump(self.scaler, scaler_filename)
            
            logging.info(f"Model saved to {model_filename}")
            logging.info(f"Scaler saved to {scaler_filename}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error saving model: {str(e)}")
            return False

def main():
    """Main function to train models for all datasets."""
    datasets = ['heart', 'kidney', 'liver', 'diabetes', 'stroke']
    
    for dataset_name in datasets:
        logging.info(f"\n{'='*50}")
        logging.info(f"Training model for {dataset_name} dataset")
        logging.info(f"{'='*50}")
        
        trainer = MedicalModelTrainer(dataset_name)
        
        if trainer.load_data():
            trainer.train_model()
        else:
            logging.error(f"Skipping {dataset_name} dataset due to loading error")

if __name__ == "__main__":
    main()