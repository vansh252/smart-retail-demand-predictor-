"""
Machine Learning Model Training for Smart Retail Demand Prediction System
Trains a RandomForestRegressor to predict product demand
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib
import os
import sys
import json
from datetime import datetime

# Add model directory to path
sys.path.append(os.path.dirname(__file__))
from data_processing import DataProcessor


class DemandPredictor:
    """Handles model training and prediction for demand forecasting"""
    
    def __init__(self, data_source='database'):
        """
        Initialize the predictor
        
        Args:
            data_source: 'database', 'excel', or 'csv'
        """
        self.model = None
        self.feature_names = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'demand_model.pkl')
        self.metadata_path = os.path.join(os.path.dirname(__file__), 'model_metadata.json')
        self.data_source = data_source
        self.processor = DataProcessor(data_source=data_source, use_validation=True)
    
    def prepare_data(self, filepath=None):
        """
        Prepare data using the data processor
        
        Args:
            filepath: Path to Excel or CSV file (if using file input)
        """
        print("=" * 60)
        print("Preparing Data for Training")
        print("=" * 60)
        
        # Run data processing pipeline
        if not self.processor.process_pipeline(filepath=filepath):
            print("Data processing failed")
            return None, None
        
        # Get features and target
        X, y, feature_names = self.processor.prepare_features()
        
        if X is None or y is None:
            print("Failed to prepare features")
            return None, None
        
        self.feature_names = feature_names
        return X, y
    
    def train_model(self, X, y, test_size=0.2, random_state=42):
        """
        Train RandomForestRegressor model
        
        Args:
            X: Feature matrix
            y: Target vector
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary with training results
        """
        print("\n" + "=" * 60)
        print("Training RandomForest Model")
        print("=" * 60)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"\nTraining set size: {len(X_train)}")
        print(f"Testing set size: {len(X_test)}")
        
        # Initialize and train model
        print("\nTraining RandomForestRegressor...")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        print("Model training completed!")
        
        # Make predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        results = {
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'test_mae': mean_absolute_error(y_test, y_test_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'n_train': len(X_train),
            'n_test': len(X_test),
            'n_features': X.shape[1]
        }
        
        # Display results
        print("\n" + "=" * 60)
        print("Model Evaluation Results")
        print("=" * 60)
        print(f"\nTraining Set:")
        print(f"  MAE:  {results['train_mae']:.2f}")
        print(f"  RMSE: {results['train_rmse']:.2f}")
        print(f"  R² Score: {results['train_r2']:.4f}")
        
        print(f"\nTesting Set:")
        print(f"  MAE:  {results['test_mae']:.2f}")
        print(f"  RMSE: {results['test_rmse']:.2f}")
        print(f"  R² Score: {results['test_r2']:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n" + "=" * 60)
        print("Top 10 Most Important Features")
        print("=" * 60)
        print(feature_importance.head(10).to_string(index=False))
        
        return results
    
    def save_model(self):
        """Save trained model and metadata to disk"""
        if self.model is None:
            print("No model to save")
            return False
        
        try:
            # Save model
            joblib.dump(self.model, self.model_path)
            print(f"\nModel saved to: {self.model_path}")
            
            # Save metadata
            metadata = {
                'feature_names': self.feature_names,
                'model_type': 'RandomForestRegressor',
                'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'n_features': len(self.feature_names)
            }
            
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            print(f"Metadata saved to: {self.metadata_path}")
            return True
            
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self):
        """Load trained model and metadata from disk"""
        try:
            # Load model
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from: {self.model_path}")
            
            # Load metadata
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.feature_names = metadata['feature_names']
            print(f"Model trained at: {metadata['trained_at']}")
            print(f"Number of features: {metadata['n_features']}")
            
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, input_data):
        """
        Make predictions on new data
        
        Args:
            input_data: Dictionary or DataFrame with input features
            
        Returns:
            Predicted demand value
        """
        if self.model is None:
            print("No model available. Please train or load a model first.")
            return None
        
        try:
            # Convert dict to DataFrame if needed
            if isinstance(input_data, dict):
                input_df = pd.DataFrame([input_data])
            else:
                input_df = input_data
            
            # Ensure all required features are present
            for feature in self.feature_names:
                if feature not in input_df.columns:
                    input_df[feature] = 0
            
            # Select features in correct order
            input_df = input_df[self.feature_names]
            
            # Make prediction
            prediction = self.model.predict(input_df)
            
            return float(prediction[0])
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None
    
    def train_and_save(self, filepath=None):
        """
        Complete training pipeline: prepare data, train, evaluate, and save
        
        Args:
            filepath: Path to Excel or CSV file (if using file input)
        """
        print("\n" + "=" * 60)
        print("SMART RETAIL DEMAND PREDICTION - MODEL TRAINING")
        print("=" * 60)
        
        # Prepare data
        X, y = self.prepare_data(filepath=filepath)
        
        if X is None or y is None:
            print("\nTraining failed: Could not prepare data")
            return False
        
        # Train model
        results = self.train_model(X, y)
        
        # Save model
        if self.save_model():
            print("\n" + "=" * 60)
            print("Training Pipeline Completed Successfully!")
            print("=" * 60)
            return True
        else:
            print("\nWarning: Model trained but failed to save")
            return False


# Example usage
if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train demand prediction model')
    parser.add_argument('--source', type=str, default='database',
                       choices=['database', 'excel', 'csv'],
                       help='Data source type')
    parser.add_argument('--file', type=str, default=None,
                       help='Path to Excel or CSV file (required for excel/csv source)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.source in ['excel', 'csv'] and args.file is None:
        print(f"Error: --file argument required when using {args.source} source")
        print(f"Usage: python train_model.py --source {args.source} --file path/to/file")
        exit(1)
    
    # Initialize predictor
    predictor = DemandPredictor(data_source=args.source)
    
    # Train and save model
    if predictor.train_and_save(filepath=args.file):
        print("\n" + "=" * 60)
        print("Testing Model Prediction")
        print("=" * 60)
        
        # Test prediction with sample data
        sample_input = {
            'price': 299.99,
            'discount': 10.0,
            'month': 3,
            'year': 2024,
            'category_Electronics': 1,
            'category_Clothing': 0,
            'category_Furniture': 0,
            'region_North': 1,
            'region_South': 0,
            'region_East': 0,
            'region_West': 0
        }
        
        predicted_demand = predictor.predict(sample_input)
        
        if predicted_demand is not None:
            print(f"\nSample Input:")
            print(f"  Price: ${sample_input['price']}")
            print(f"  Discount: {sample_input['discount']}%")
            print(f"  Month: {sample_input['month']}")
            print(f"  Category: Electronics")
            print(f"  Region: North")
            print(f"\nPredicted Demand: {predicted_demand:.0f} units")
