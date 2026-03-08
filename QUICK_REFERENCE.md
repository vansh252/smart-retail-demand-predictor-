# Quick Reference Guide
# Smart Retail Demand Prediction System

## 🚀 Quick Start Commands

### Initial Setup (Run Once)
```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database in .env file
# Edit .env with your MySQL credentials

# 4. Setup database
mysql -u root -p < database\schema.sql

# 5. Train the model
python model\train_model.py
```

### Run the System
```bash
# Terminal 1: Start Backend API
python backend\app.py

# Terminal 2: Start Dashboard (keep backend running)
streamlit run dashboard\app.py
```

## 📋 Common Commands

### Excel Data Processing (New!)
```bash
# Interactive Excel processor
python model\process_excel.py

# Process specific Excel file
python model\process_excel.py data\your_file.xlsx

# Create sample messy data (learning)
python model\process_excel.py
# Choose option 2

# Create clean template
python model\process_excel.py
# Choose option 3
```

### Database Operations
```bash
# Connect to MySQL
mysql -u root -p

# View sales data
mysql -u root -p retail_demand_db -e "SELECT * FROM sales_data LIMIT 10;"

# Count records
mysql -u root -p retail_demand_db -e "SELECT COUNT(*) FROM sales_data;"

# Generate more sample data
python data\generate_sample_data.py
```

### Model Operations
```bash
# Train/retrain model from database
python model\train_model.py

# Train from Excel file
python model\train_model.py --source excel --file data\your_data.xlsx

# Train from CSV file
python model\train_model.py --source csv --file data\cleaned_data.csv

# Process data only
python model\data_processing.py

# Test database connection
python database\db_connection.py
```

### API Testing
```bash
# Test API health
curl http://127.0.0.1:5000/

# Make prediction (PowerShell)
$body = @{
    price = 299.99
    discount = 10.0
    month = 3
    category = "Electronics"
    region = "North"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" -Method Post -Body $body -ContentType "application/json"
```

## 🗂️ File Structure Overview

```
Project Root
│
├── 📁 data/                    # Data storage
│   ├── generate_sample_data.py # Sample data generator
│   └── processed_*.csv        # Processed data (auto-generated)
│
├── 📁 database/               # Database layer
│   ├── schema.sql             # Database schema
│   └── db_connection.py       # DB connection module
│
├── 📁 model/                  # Machine learning
│   ├── data_processing.py     # Data preprocessing
│   ├── train_model.py         # Model training
│   ├── demand_model.pkl       # Trained model (auto-generated)
│   └── model_metadata.json    # Model info (auto-generated)
│
├── 📁 backend/                # Flask API
│   └── app.py                 # REST API server
│
├── 📁 dashboard/              # Streamlit UI
│   └── app.py                 # Dashboard app
│
├── 📄 config.py               # Central configuration
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env.example            # Environment template
├── 📄 .env                    # Your config (create this)
├── 📄 setup.bat              # Windows setup script
├── 📄 setup.ps1              # PowerShell setup script
└── 📄 README.md              # Full documentation
```

## 🔑 Key Features by Component

### Database (MySQL)
- Stores historical sales data
- Fields: product_id, sale_date, region, category, quantity_sold, price, discount
- Sample data included
- Indexed for performance

### Data Processing (model/data_processing.py)
- Loads data from database
- Cleans missing values
- Extracts date features (month, year, quarter)
- One-hot encodes categories and regions
- Saves processed data

### ML Model (model/train_model.py)
- RandomForestRegressor
- Features: price, discount, month, category, region
- Target: quantity_sold
- Metrics: MAE, RMSE, R² score
- Saves model with joblib

### Backend API (backend/app.py)
- Flask REST API
- Endpoints:
  * GET / - Health check
  * GET /model/info - Model details
  * POST /predict - Single prediction
  * POST /batch_predict - Multiple predictions
- CORS enabled
- Input validation

### Dashboard (dashboard/app.py)
- 3 pages: Analytics, Prediction, Data View
- Interactive charts with Plotly
- Real-time predictions via API
- Data filtering and export
- Responsive design

## 🎯 Typical Workflow

1. **Setup** (One time)
   - Install dependencies
   - Configure database
   - Load sample data
   - Train initial model

2. **Daily Use**
   - Start backend API
   - Start dashboard
   - Make predictions
   - View analytics

3. **Model Updates** (As needed)
   - Add new data to database
   - Retrain model
   - Restart backend

## 🔧 Configuration Files

### .env (Create from .env.example)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=retail_demand_db
```

### requirements.txt
All Python dependencies:
- numpy, pandas (data processing)
- scikit-learn (ML)
- mysql-connector-python (database)
- flask, flask-cors (API)
- streamlit, plotly (dashboard)

## 📊 Sample Prediction Request

### Input Format
```json
{
  "price": 299.99,
  "discount": 10.0,
  "month": 3,
  "category": "Electronics",
  "region": "North"
}
```

### Response Format
```json
{
  "status": "success",
  "predicted_demand": 55.5,
  "unit": "units",
  "inputs": { ... }
}
```

## ⚠️ Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| DB connection error | Check .env credentials |
| Model not found | Run `python model\train_model.py` |
| API not responding | Check if backend is running on port 5000 |
| Port in use | Change port or kill existing process |

## 📞 Help Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Check MySQL status
mysql --version

# View active Python processes
tasklist | findstr python

# Kill process on port 5000 (if needed)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## 🎓 Learning Path

1. Start with README.md for full documentation
2. Explore database/schema.sql to understand data structure
3. Run model/train_model.py to see ML pipeline
4. Test backend/app.py API endpoints
5. Use dashboard/app.py for interactive exploration
6. Modify config.py for customization

---

**For detailed explanations, see README.md**
