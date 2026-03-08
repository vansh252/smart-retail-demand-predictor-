"""
Flask Backend API for Smart Retail Demand Prediction System
Provides REST API endpoints for demand prediction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys
import os
import io
import pandas as pd

# Add model directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
from train_model import DemandPredictor

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Upload config
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Global predictor instance
predictor = None

def initialize_predictor():
    """Initialize and load the trained model"""
    global predictor
    try:
        predictor = DemandPredictor()
        if predictor.load_model():
            print("Model loaded successfully")
            return True
        else:
            print("Failed to load model. Please train the model first.")
            return False
    except Exception as e:
        print(f"Error initializing predictor: {e}")
        return False


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Smart Retail Demand Prediction API',
        'endpoints': {
            '/': 'Health check',
            '/predict': 'POST - Make demand prediction',
            '/model/info': 'GET - Get model information'
        }
    })


@app.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    if predictor is None or predictor.model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded'
        }), 500
    
    try:
        return jsonify({
            'status': 'success',
            'model_type': 'RandomForestRegressor',
            'n_features': len(predictor.feature_names),
            'features': predictor.feature_names
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict product demand
    
    Expected JSON body:
    {
        "price": 299.99,
        "discount": 10.0,
        "month": 3,
        "category": "Electronics",
        "region": "North"
    }
    
    Returns:
    {
        "status": "success",
        "predicted_demand": 55.5,
        "inputs": {...}
    }
    """
    if predictor is None or predictor.model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded. Please train the model first.'
        }), 500
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['price', 'discount', 'month', 'category', 'region']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }), 400
        
        # Prepare input features
        input_features = prepare_input_features(data)
        
        # Make prediction
        predicted_demand = predictor.predict(input_features)
        
        if predicted_demand is None:
            return jsonify({
                'status': 'error',
                'message': 'Prediction failed'
            }), 500
        
        # Return response
        return jsonify({
            'status': 'success',
            'predicted_demand': round(predicted_demand, 2),
            'unit': 'units',
            'inputs': {
                'price': data['price'],
                'discount': data['discount'],
                'month': data['month'],
                'category': data['category'],
                'region': data['region']
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def prepare_input_features(data):
    """
    Prepare input features from request data
    
    Args:
        data: Dictionary with user input
        
    Returns:
        Dictionary with one-hot encoded features
    """
    # Extract base features
    features = {
        'price': float(data.get('price', 0)),
        'discount': float(data.get('discount', 0)),
        'month': int(data.get('month', 1)),
        'year': int(data.get('year', 2024))
    }
    
    # One-hot encode category
    category = data.get('category', '')
    categories = ['Electronics', 'Clothing', 'Furniture']
    for cat in categories:
        features[f'category_{cat}'] = 1 if category == cat else 0
    
    # One-hot encode region
    region = data.get('region', '')
    regions = ['North', 'South', 'East', 'West']
    for reg in regions:
        features[f'region_{reg}'] = 1 if region == reg else 0
    
    return features


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Make predictions for multiple inputs
    
    Expected JSON body:
    {
        "predictions": [
            {"price": 299.99, "discount": 10, "month": 3, "category": "Electronics", "region": "North"},
            {"price": 49.99, "discount": 5, "month": 4, "category": "Clothing", "region": "South"}
        ]
    }
    """
    if predictor is None or predictor.model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded'
        }), 500
    
    try:
        data = request.get_json()
        predictions_input = data.get('predictions', [])
        
        if not predictions_input:
            return jsonify({
                'status': 'error',
                'message': 'No prediction inputs provided'
            }), 400
        
        results = []
        for input_data in predictions_input:
            input_features = prepare_input_features(input_data)
            predicted_demand = predictor.predict(input_features)
            
            results.append({
                'inputs': input_data,
                'predicted_demand': round(predicted_demand, 2) if predicted_demand else None
            })
        
        return jsonify({
            'status': 'success',
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/upload', methods=['POST'])
def upload_data():
    """
    Upload a CSV or Excel file for processing.
    Returns file info and a preview of the data.
    """
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Invalid file type. Use CSV, XLSX, or XLS'}), 400

    try:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()

        if ext == 'csv':
            df = pd.read_csv(file.stream)
        else:
            engine = 'openpyxl' if ext == 'xlsx' else 'xlrd'
            df = pd.read_excel(file.stream, engine=engine)

        # Save raw upload
        save_path = os.path.join(DATA_DIR, f'upload_{filename}')
        df.to_csv(save_path.rsplit('.', 1)[0] + '.csv', index=False)

        return jsonify({
            'status': 'success',
            'filename': filename,
            'rows': len(df),
            'columns': list(df.columns),
            'preview': df.head(5).to_dict(orient='records'),
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Starting Smart Retail Demand Prediction API")
    print("=" * 60)
    
    # Initialize predictor
    if initialize_predictor():
        print("\n" + "=" * 60)
        print("API Server Ready")
        print("=" * 60)
        print("\nEndpoints:")
        print("  GET  /              - Health check")
        print("  GET  /model/info    - Model information")
        print("  POST /predict       - Single prediction")
        print("  POST /batch_predict - Batch predictions")
        print("\n" + "=" * 60)
        
        # Start Flask server
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True
        )
    else:
        print("\nERROR: Could not initialize predictor")
        print("Please run train_model.py first to create the model")
