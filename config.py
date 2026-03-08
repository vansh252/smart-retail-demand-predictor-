"""
Configuration Module for Smart Retail Demand Prediction System
Central configuration for all components
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration"""
    
    # Project
    PROJECT_NAME = "Smart Retail Demand Prediction System"
    VERSION = "1.0.0"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'retail_demand_db')
    
    # Flask Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Model Configuration
    MODEL_PATH = os.path.join(MODEL_DIR, 'demand_model.pkl')
    METADATA_PATH = os.path.join(MODEL_DIR, 'model_metadata.json')
    PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_sales_data.csv')
    
    # ML Parameters
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    N_ESTIMATORS = 100
    MAX_DEPTH = 10
    MIN_SAMPLES_SPLIT = 5
    MIN_SAMPLES_LEAF = 2
    
    # Features
    NUMERIC_FEATURES = ['price', 'discount', 'month', 'year']
    CATEGORICAL_FEATURES = ['category', 'region']
    TARGET_COLUMN = 'quantity_sold'
    
    # Categories and Regions
    CATEGORIES = ['Electronics', 'Clothing', 'Furniture']
    REGIONS = ['North', 'South', 'East', 'West']
    
    # API Configuration
    API_TIMEOUT = 5
    API_URL = f"http://{FLASK_HOST}:{FLASK_PORT}"
    
    # Streamlit Configuration
    STREAMLIT_THEME = "light"
    STREAMLIT_PORT = 8501


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DB_NAME = 'retail_demand_test_db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env='default'):
    """
    Get configuration based on environment
    
    Args:
        env: Environment name ('development', 'production', 'testing')
        
    Returns:
        Configuration class
    """
    return config.get(env, config['default'])


# Example usage
if __name__ == "__main__":
    cfg = get_config('development')
    
    print("=" * 60)
    print("Configuration Settings")
    print("=" * 60)
    print(f"\nProject: {cfg.PROJECT_NAME}")
    print(f"Version: {cfg.VERSION}")
    print(f"\nDatabase: {cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}")
    print(f"API: {cfg.API_URL}")
    print(f"Model Path: {cfg.MODEL_PATH}")
    print(f"\nCategories: {', '.join(cfg.CATEGORIES)}")
    print(f"Regions: {', '.join(cfg.REGIONS)}")
