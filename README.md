# 📊 Smart Retail Demand Prediction System

An MVP machine learning system that predicts product demand using historical retail sales data.

## 🎯 Overview

This system uses machine learning to predict retail product demand based on factors like price, discount, category, region, and time of year. It features a Flask REST API for predictions and an interactive Streamlit dashboard for visualization and interaction.

## 🏗️ Tech Stack

- **Python 3.8+** - Core programming language
- **MySQL** - Database for storing sales data
- **Pandas** - Data processing and manipulation
- **NumPy** - Numerical operations
- **Scikit-learn** - Machine learning (RandomForestRegressor)
- **Flask** - Backend REST API
- **Streamlit** - Interactive dashboard
- **Joblib** - Model serialization
- **Plotly** - Interactive visualizations
- **OpenPyXL/XLRD** - Excel file support (.xlsx, .xls)

## ✨ New Feature: Excel Data Support

The system now accepts **Excel files** with comprehensive data validation and cleaning! This provides hands-on experience with real-world data quality issues.

**Features:**
- ✅ Load data from Excel (.xlsx, .xls)
- ✅ Comprehensive data validation (schema, types, ranges)
- ✅ Automatic data cleaning (missing values, outliers, formatting)
- ✅ Detailed quality reports
- ✅ Handle messy real-world data
- ✅ Educational experience with data preprocessing

**Quick Start with Excel:**
```bash
# Interactive Excel processor
python model/process_excel.py

# Train model from Excel file
python model/train_model.py --source excel --file your_data.xlsx
```

**See [EXCEL_GUIDE.md](EXCEL_GUIDE.md) for detailed documentation.**

## 📁 Project Structure

```
hackthone 4/
│
├── data/                          # Data storage
│   └── processed_sales_data.csv   # Processed data (generated)
│
├── database/                      # Database layer
│   ├── schema.sql                 # MySQL schema and sample data
│   └── db_connection.py           # Database connection module
│
├── model/                         # Machine learning
│   ├── data_processing.py         # Data preprocessing pipeline
│   ├── train_model.py             # Model training script
│   ├── demand_model.pkl           # Trained model (generated)
│   └── model_metadata.json        # Model metadata (generated)
│
├── backend/                       # Flask API
│   └── app.py                     # REST API server
│
├── dashboard/                     # Streamlit UI
│   └── app.py                     # Dashboard application
│
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- Git (optional)

### 2. Database Setup

**Start MySQL server and create the database:**

```sql
-- Login to MySQL
mysql -u root -p

-- Run the schema file
source database/schema.sql
```

Or manually:

```sql
CREATE DATABASE IF NOT EXISTS retail_demand_db;
USE retail_demand_db;

-- Copy and paste the contents of database/schema.sql
```

### 3. Python Environment Setup

**Create a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

**Create `.env` file from the template:**

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**Edit `.env` with your MySQL credentials:**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=retail_demand_db
```

### 5. Train the Machine Learning Model

**Option A: Train from Database (Default)**

```bash
python model/train_model.py
```

**Option B: Train from Excel File (New!)**

```bash
# First, process your Excel file
python model/process_excel.py

# Then train from Excel with validation
python model/train_model.py --source excel --file data/your_sales_data.xlsx

# Or train from cleaned CSV
python model/train_model.py --source csv --file data/cleaned_data_*.csv
```

This will:
- Load data from the specified source
- Process and clean the data (with comprehensive validation for Excel)
- Train a RandomForestRegressor
- Save the model as `model/demand_model.pkl`
- Display evaluation metrics (MAE, RMSE, R² score)

**Expected output:**
```
Training RandomForest Model
Training set size: XX
Testing set size: XX
Model training completed!

Model Evaluation Results
Testing Set:
  MAE:  XX.XX
  RMSE: XX.XX
  R² Score: 0.XXXX
```

## 🎮 Usage

### Option A: Using Database (Default)

#### Run the Backend API

**Terminal 1:**

```bash
python backend/app.py
```

The API will start at `http://127.0.0.1:5000`

**Available endpoints:**

- `GET /` - Health check
- `GET /model/info` - Model information
- `POST /predict` - Make prediction
- `POST /batch_predict` - Batch predictions

**Example prediction request:**

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "price": 299.99,
    "discount": 10.0,
    "month": 3,
    "category": "Electronics",
    "region": "North"
  }'
```

**Example response:**

```json
{
  "status": "success",
  "predicted_demand": 55.5,
  "unit": "units",
  "inputs": {
    "price": 299.99,
    "discount": 10.0,
    "month": 3,
    "category": "Electronics",
    "region": "North"
  }
}
```

### Run the Dashboard

**Terminal 2 (keep backend running):**

```bash
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501`

**Dashboard features:**

1. **📈 Analytics Page**
   - Total sales metrics
   - Sales by category and region
   - Time series trends
   - Price vs quantity correlation

2. **🔮 Prediction Page**
   - Input form for prediction parameters
   - Real-time API calls
   - Interactive result display
   - Input summary

3. **📋 Data View Page**
   - Filterable sales data table
   - Export to CSV
   - Search and filter options

## 📊 Database Schema

### `sales_data` Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| product_id | VARCHAR(50) | Product identifier |
| sale_date | DATE | Date of sale |
| region | VARCHAR(100) | Sales region |
| category | VARCHAR(100) | Product category |
| quantity_sold | INT | Number of units sold |
| price | DECIMAL(10,2) | Product price |
| discount | DECIMAL(5,2) | Discount percentage |
| created_at | TIMESTAMP | Record creation time |

## 🔧 Features

### Data Processing
- ✅ Automatic data loading from MySQL
- ✅ Missing value handling
- ✅ Date feature extraction (month, year, quarter)
- ✅ Categorical encoding (one-hot)
- ✅ Data quality checks

### Machine Learning
- ✅ RandomForestRegressor model
- ✅ Feature importance analysis
- ✅ Model evaluation (MAE, RMSE, R²)
- ✅ Model persistence with joblib
- ✅ Metadata tracking

### Backend API
- ✅ RESTful Flask API
- ✅ CORS enabled
- ✅ Single and batch predictions
- ✅ Error handling
- ✅ Input validation

### Dashboard
- ✅ Interactive visualizations
- ✅ Real-time predictions
- ✅ Sales analytics
- ✅ Data filtering and export
- ✅ Responsive design

## 📈 Model Performance

The RandomForestRegressor is evaluated using:

- **MAE (Mean Absolute Error)** - Average prediction error in units
- **RMSE (Root Mean Squared Error)** - Penalizes larger errors more
- **R² Score** - Proportion of variance explained (0-1, higher is better)

Typical results for the MVP with sample data:
- Test R² Score: 0.75-0.85
- Test MAE: 10-20 units

## 🔍 Testing the System

### 1. Verify Database Connection

```bash
python database/db_connection.py
```

Should output sales data from the database.

### 2. Test Data Processing

```bash
python model/data_processing.py
```

Should process data and save to `data/processed_sales_data.csv`.

### 3. Test Model Training

```bash
python model/train_model.py
```

Should train model and save to `model/demand_model.pkl`.

### 4. Test API

```bash
# Start API
python backend/app.py

# In another terminal, test endpoint
curl http://127.0.0.1:5000/
```

### 5. Test Dashboard

```bash
streamlit run dashboard/app.py
```

Navigate through all three pages to ensure functionality.

## 🐛 Troubleshooting

### Database Connection Issues

```
Error: Access denied for user 'root'@'localhost'
```

**Solution:** Check your MySQL credentials in `.env` file.

### Model Not Found

```
Error: Model not loaded. Please train the model first.
```

**Solution:** Run `python model/train_model.py` to create the model.

### API Connection Failed

```
❌ API Not Available
```

**Solution:** Ensure Flask server is running on port 5000.

### Import Errors

```
ModuleNotFoundError: No module named 'X'
```

**Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`.

### Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution:** Change port in code or kill process using the port.

## 📝 Adding New Data

### Via MySQL

```sql
INSERT INTO sales_data (product_id, sale_date, region, category, quantity_sold, price, discount)
VALUES ('P006', '2024-04-01', 'North', 'Electronics', 80, 399.99, 15.00);
```

### Via Python

```python
from database.db_connection import DatabaseConnection

db = DatabaseConnection()
if db.connect():
    db.insert_sale(
        product_id='P006',
        sale_date='2024-04-01',
        region='North',
        category='Electronics',
        quantity_sold=80,
        price=399.99,
        discount=15.00
    )
    db.disconnect()
```

After adding new data, retrain the model:

```bash
python model/train_model.py
```

## 🎯 Future Enhancements

- [ ] Add more ML algorithms (XGBoost, Neural Networks)
- [ ] Implement time series forecasting
- [ ] Add user authentication
- [ ] Deploy to cloud (AWS, Azure, GCP)
- [ ] Add A/B testing capabilities
- [ ] Implement automated retraining pipeline
- [ ] Add more visualization options
- [ ] Create mobile app version

## 📄 License

This project is created for educational purposes as an MVP demonstration.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify database connectivity

## 🎓 Learning Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Built with ❤️ for retail demand forecasting**
