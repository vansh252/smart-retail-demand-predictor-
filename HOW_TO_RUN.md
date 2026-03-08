# 🚀 HOW TO RUN THE PROJECT - Step by Step Guide
# Smart Retail Demand Prediction System

## ⚡ QUICK START (5 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**If you get errors, install individually:**
```bash
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install openpyxl==3.1.2
pip install xlrd==2.0.1
pip install scikit-learn==1.3.0
pip install joblib==1.3.2
pip install mysql-connector-python==8.1.0
pip install python-dotenv==1.0.0
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install streamlit==1.26.0
pip install plotly==5.16.1
pip install requests==2.31.0
pip install Werkzeug==2.3.7
```

### Step 2A: Try Excel First (EASIEST - No Database Needed!)
```bash
# Run the Excel processor
python model/process_excel.py
```

**Choose Option 2** - Creates sample data automatically

Then:
```bash
# Train model with the cleaned data
python model/train_model.py --source csv --file data/cleaned_data_*.csv
```

**Or use the generated file name, example:**
```bash
python model/train_model.py --source csv --file "data/cleaned_data_20260307_120000.csv"
```

### Step 2B: OR Use Database (Requires MySQL)

**Only if you have MySQL installed:**

1. **Start MySQL:**
   - Open MySQL Workbench or command line
   - Login: `mysql -u root -p`

2. **Create Database:**
```bash
# In MySQL:
source database/schema.sql

# Or manually:
mysql -u root -p < database/schema.sql
```

3. **Configure .env file:**
```bash
# Create .env from template
copy .env.example .env

# Edit .env and add your MySQL password:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_PASSWORD_HERE
DB_NAME=retail_demand_db
```

4. **Train model:**
```bash
python model/train_model.py
```

### Step 3: Start Backend API
```bash
python backend/app.py
```

**You should see:**
```
Starting Smart Retail Demand Prediction API
Model loaded successfully
API Server Ready

Endpoints:
  GET  /              - Health check
  GET  /model/info    - Model information
  POST /predict       - Single prediction
  POST /batch_predict - Batch predictions
```

**Keep this terminal open!**

### Step 4: Start Dashboard (New Terminal)

Open a NEW terminal, activate venv, and run:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run dashboard
streamlit run dashboard/app.py
```

**Dashboard will open automatically at:** `http://localhost:8501`

### Step 5: Use the System! 🎉

The browser will open with your dashboard showing:
- 📈 **Analytics Page** - View sales charts
- 🔮 **Prediction Page** - Make demand predictions
- 📋 **Data View** - Browse and filter data

---

## 🔧 TROUBLESHOOTING

### Problem: "No module named 'X'"
**Solution:**
```bash
pip install X
```
Or reinstall all:
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: "Model not loaded"
**Solution:**
You need to train the model first!
```bash
# Easiest way - use sample Excel data:
python model/process_excel.py
# Choose option 2, then:
python model/train_model.py --source csv --file "data/cleaned_data_*.csv"
```

### Problem: "Database connection failed"
**Solution:**
Use Excel instead (no database needed):
```bash
python model/process_excel.py
# Choose option 2
python model/train_model.py --source csv --file "data/cleaned_data_*.csv"
```

### Problem: "Port already in use"
**Solution:**
```bash
# Kill process on port 5000:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or change port in backend/app.py (line with app.run)
```

### Problem: "Streamlit won't start"
**Solution:**
```bash
# Make sure you're in the right directory:
cd "c:\Users\singh\OneDrive\Desktop\hackthone 4"

# Make sure venv is activated:
venv\Scripts\activate

# Try:
python -m streamlit run dashboard/app.py
```

### Problem: Excel file errors
**Solution:**
```bash
pip install openpyxl xlrd --upgrade
```

---

## 📝 COMPLETE WORKFLOW OPTIONS

### Option A: Excel Only (RECOMMENDED FOR FIRST TIME)

This is the easiest - no database setup needed!

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data and train model
python model/process_excel.py
# Choose option 2 (creates sample messy data)
# It will automatically clean it

# 3. Train model with cleaned data
# Note: Check the data folder for the actual filename
dir data
# Look for: cleaned_data_YYYYMMDD_HHMMSS.csv
python model/train_model.py --source csv --file "data/cleaned_data_20260307_120000.csv"

# 4. Start backend (Terminal 1)
python backend/app.py

# 5. Start dashboard (Terminal 2 - new window)
streamlit run dashboard/app.py
```

### Option B: Database Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup MySQL
mysql -u root -p
# Enter password, then:
source database/schema.sql;
exit;

# 3. Configure .env
copy .env.example .env
# Edit .env with your MySQL password

# 4. Train model
python model/train_model.py

# 5. Start backend (Terminal 1)
python backend/app.py

# 6. Start dashboard (Terminal 2)
streamlit run dashboard/app.py
```

### Option C: Your Own Excel Data

```bash
# 1. Create Excel file with columns:
#    product_id, sale_date, region, category, quantity_sold, price, discount

# 2. Process your file
python model/process_excel.py
# Choose option 1, enter your file path

# 3. Train model
python model/train_model.py --source csv --file "data/cleaned_data_*.csv"

# 4. Start backend
python backend/app.py

# 5. Start dashboard
streamlit run dashboard/app.py
```

---

## ✅ VERIFICATION CHECKLIST

Before running, make sure:

- [ ] Virtual environment activated (`venv\Scripts\activate`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Model trained (one of the train_model.py commands)
- [ ] Backend running on port 5000
- [ ] Dashboard running on port 8501

---

## 🎯 RECOMMENDED FIRST RUN

**Copy and paste these commands one by one:**

```bash
# Make sure you're in the project folder
cd "c:\Users\singh\OneDrive\Desktop\hackthone 4"

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create sample data and process it
python model/process_excel.py
```

**When menu appears, press:** `2` then `Enter` (creates sample messy data)
**Then press:** `y` then `Enter` (process the file)
**Then press:** `n` then `Enter` (exit)

```bash
# Check what files were created
dir data

# Train model with the cleaned data (use the actual filename you see)
python model/train_model.py --source csv --file "data/cleaned_data_20260307_120000.csv"
```

**After training completes:**

```bash
# Start backend
python backend/app.py
```

**Open a NEW terminal window and run:**

```bash
cd "c:\Users\singh\OneDrive\Desktop\hackthone 4"
venv\Scripts\activate
streamlit run dashboard/app.py
```

**Your dashboard should open automatically!** 🎉

---

## 💡 TIPS

1. **First time?** Use Excel option - it's easiest
2. **Keep terminals open** - Don't close backend while using dashboard
3. **Check the data folder** - All outputs are saved there with timestamps
4. **Review reports** - Check `data/data_quality_report.txt` for insights
5. **Having issues?** The Excel sample data (option 2) always works!

---

## 📞 STILL STUCK?

Run these diagnostic commands:

```bash
# Check Python version (need 3.8+)
python --version

# Check if dependencies are installed
pip list

# Check if model file exists
dir model\*.pkl

# Check if cleaned data exists
dir data\*.csv

# Test database connection (if using MySQL)
python database/db_connection.py
```

Send me the output if you need help!

---

## 🎓 WHAT EACH COMMAND DOES

| Command | What It Does |
|---------|-------------|
| `pip install -r requirements.txt` | Installs all Python libraries needed |
| `python model/process_excel.py` | Interactive tool to create/process Excel data |
| `python model/train_model.py` | Trains the AI model to predict demand |
| `python backend/app.py` | Starts the API server (handles predictions) |
| `streamlit run dashboard/app.py` | Starts the web dashboard (UI) |

---

**Ready to start? Follow the RECOMMENDED FIRST RUN section above!** 🚀
