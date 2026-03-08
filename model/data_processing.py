"""
Data Processing Module for Smart Retail Demand Prediction System
Handles data loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add database directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from db_connection import DatabaseConnection
from data_validator import DataValidator


class DataProcessor:
    """Processes sales data for machine learning"""
    
    def __init__(self, data_source='database', use_validation=True):
        """
        Initialize data processor
        
        Args:
            data_source: 'database', 'csv', or 'excel'
            use_validation: Whether to use comprehensive data validation
        """
        self.data_source = data_source
        self.raw_data = None
        self.processed_data = None
        self.use_validation = use_validation
        self.validator = None
    
    def load_data_from_database(self):
        """Load sales data from MySQL database"""
        print("Loading data from database...")
        db = DatabaseConnection()
        
        if db.connect():
            self.raw_data = db.get_all_sales_data()
            db.disconnect()
            
            if self.raw_data is not None:
                print(f"Loaded {len(self.raw_data)} records from database")
                return True
            else:
                print("Failed to load data from database")
                return False
        return False
    
    def load_data_from_csv(self, filepath):
        """Load sales data from CSV file"""
        print(f"Loading data from CSV: {filepath}")
        try:
            self.raw_data = pd.read_csv(filepath)
            print(f"Loaded {len(self.raw_data)} records from CSV")
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False
    
    def load_data_from_excel(self, filepath, use_validator=True):
        """
        Load and validate sales data from Excel file
        
        Args:
            filepath: Path to Excel file (.xlsx or .xls)
            use_validator: Use comprehensive validation (recommended)
            
        Returns:
            bool: Success status
        """
        print(f"Loading data from Excel: {filepath}")
        
        if use_validator and self.use_validation:
            # Use comprehensive validator
            self.validator = DataValidator(verbose=True)
            
            # Load file
            df = self.validator.load_excel_file(filepath)
            if df is None:
                return False
            
            # Run full validation
            self.validator.validate_schema()
            self.validator.validate_data_types()
            self.validator.check_duplicates()
            
            # Clean data
            print("\nStarting data cleaning process...")
            cleaned_df = self.validator.clean_data()
            
            if cleaned_df is None:
                print("Data cleaning failed")
                return False
            
            # Generate report
            report_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            os.makedirs(report_dir, exist_ok=True)
            report_file = os.path.join(report_dir, 'data_quality_report.txt')
            self.validator.generate_report(report_file)
            
            self.raw_data = cleaned_df
            print(f"\n✓ Successfully loaded and cleaned {len(self.raw_data)} records from Excel")
            return True
            
        else:
            # Simple load without validation
            try:
                self.raw_data = pd.read_excel(filepath)
                print(f"Loaded {len(self.raw_data)} records from Excel")
                return True
            except Exception as e:
                print(f"Error loading Excel: {e}")
                return False
    
    def clean_data(self):
        """Clean missing values and handle data quality issues"""
        print("\nCleaning data...")
        
        if self.raw_data is None:
            print("No data to clean")
            return False
        
        df = self.raw_data.copy()
        
        # Display initial data info
        print(f"Initial shape: {df.shape}")
        print(f"Missing values:\n{df.isnull().sum()}")
        
        # Handle missing values
        # Fill numeric columns with median
        numeric_cols = ['quantity_sold', 'price', 'discount']
        for col in numeric_cols:
            if col in df.columns:
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        categorical_cols = ['product_id', 'region', 'category']
        for col in categorical_cols:
            if col in df.columns:
                df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
        
        # Remove duplicates
        df.drop_duplicates(inplace=True)
        
        # Remove rows with negative or zero quantity_sold
        if 'quantity_sold' in df.columns:
            df = df[df['quantity_sold'] > 0]
        
        print(f"Cleaned shape: {df.shape}")
        self.raw_data = df
        return True
    
    def extract_date_features(self):
        """Extract month, year, and other time-based features from sale_date"""
        print("\nExtracting date features...")
        
        if self.raw_data is None:
            print("No data available")
            return False
        
        df = self.raw_data.copy()
        
        # Convert sale_date to datetime
        if 'sale_date' in df.columns:
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            
            # Extract features
            df['month'] = df['sale_date'].dt.month
            df['year'] = df['sale_date'].dt.year
            df['day_of_week'] = df['sale_date'].dt.dayofweek
            df['quarter'] = df['sale_date'].dt.quarter
            
            print("Extracted: month, year, day_of_week, quarter")
        else:
            print("Warning: 'sale_date' column not found")
        
        self.raw_data = df
        return True
    
    def encode_categorical_features(self):
        """Encode categorical features for machine learning"""
        print("\nEncoding categorical features...")
        
        if self.raw_data is None:
            print("No data available")
            return False
        
        df = self.raw_data.copy()
        
        # One-hot encode category and region
        if 'category' in df.columns:
            category_dummies = pd.get_dummies(df['category'], prefix='category')
            df = pd.concat([df, category_dummies], axis=1)
        
        if 'region' in df.columns:
            region_dummies = pd.get_dummies(df['region'], prefix='region')
            df = pd.concat([df, region_dummies], axis=1)
        
        print(f"Final shape after encoding: {df.shape}")
        self.processed_data = df
        return True
    
    def prepare_features(self, target_col='quantity_sold'):
        """
        Prepare feature matrix (X) and target vector (y)
        
        Args:
            target_col: Name of the target column
            
        Returns:
            X, y, feature_names
        """
        print("\nPreparing features for ML...")
        
        if self.processed_data is None:
            print("No processed data available")
            return None, None, None
        
        df = self.processed_data.copy()
        
        # Define feature columns
        # Base numeric features
        feature_cols = ['price', 'discount', 'month', 'year']
        
        # Add encoded categorical features
        category_cols = [col for col in df.columns if col.startswith('category_')]
        region_cols = [col for col in df.columns if col.startswith('region_')]
        
        feature_cols.extend(category_cols)
        feature_cols.extend(region_cols)
        
        # Filter only existing columns
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        # Prepare X and y
        X = df[feature_cols].copy()
        y = df[target_col].copy() if target_col in df.columns else None
        
        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape if y is not None else 'None'}")
        print(f"Feature columns: {feature_cols}")
        
        return X, y, feature_cols
    
    def get_processed_dataframe(self):
        """Return the processed dataframe"""
        return self.processed_data
    
    def save_processed_data(self, filepath):
        """Save processed data to CSV"""
        if self.processed_data is not None:
            self.processed_data.to_csv(filepath, index=False)
            print(f"\nProcessed data saved to: {filepath}")
            return True
        return False
    
    def process_pipeline(self, filepath=None):
        """
        Execute full data processing pipeline
        
        Args:
            filepath: Path to CSV or Excel file (if using file input)
        """
        print("=" * 60)
        print("Starting Data Processing Pipeline")
        print("=" * 60)
        
        # Load data
        if self.data_source == 'database':
            if not self.load_data_from_database():
                return False
        elif self.data_source == 'excel':
            if not filepath:
                print("Error: Excel file path required")
                return False
            if not self.load_data_from_excel(filepath):
                return False
        elif self.data_source == 'csv':
            if not filepath:
                print("Error: CSV file path required")
                return False
            if not self.load_data_from_csv(filepath):
                return False
        else:
            print(f"Error: Unknown data source '{self.data_source}'")
            return False
        
        # If validator was used, data is already cleaned
        if self.validator is not None:
            print("\nData already cleaned by validator, proceeding with feature engineering...")
        else:
            # Clean data
            if not self.clean_data():
                return False
        
        # Extract date features
        if not self.extract_date_features():
            return False
        
        # Encode categorical features
        if not self.encode_categorical_features():
            return False
        
        print("\n" + "=" * 60)
        print("Data Processing Pipeline Completed Successfully")
        print("=" * 60)
        
        return True


# Example usage
if __name__ == "__main__":
    # Initialize processor
    processor = DataProcessor(data_source='database')
    
    # Run full pipeline
    if processor.process_pipeline():
        # Prepare features
        X, y, feature_names = processor.prepare_features()
        
        if X is not None and y is not None:
            print("\n" + "=" * 60)
            print("Data Summary:")
            print("=" * 60)
            print(f"Total samples: {len(X)}")
            print(f"Number of features: {len(feature_names)}")
            print(f"\nTarget variable (quantity_sold) statistics:")
            print(y.describe())
            
            # Save processed data
            output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed_sales_data.csv')
            processor.save_processed_data(output_path)
