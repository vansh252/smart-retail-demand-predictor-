# Smart Retail Demand Prediction - Complete Setup and Run Script
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Smart Retail Demand Prediction System - Complete Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Activate virtual environment
Write-Host "Step 1: Activating Virtual Environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Step 2: Install compatible packages
Write-Host "`nStep 2: Installing Compatible Packages..." -ForegroundColor Yellow
Write-Host "Installing core ML packages..." -ForegroundColor Gray
pip install --quiet --upgrade pip
pip install --quiet 'numpy>=1.24,<2' 'pandas>=2.0,<3' 'scikit-learn>=1.3,<2' joblib

Write-Host "Installing web framework packages..." -ForegroundColor Gray
pip install --quiet flask flask-cors

Write-Host "Installing dashboard packages..." -ForegroundColor Gray  
pip install --quiet 'streamlit>=1.26,<2' plotly requests

Write-Host "Installing Excel support..." -ForegroundColor Gray
pip install --quiet openpyxl xlrd

Write-Host "`n✓ All packages installed successfully!" -ForegroundColor Green

# Step 3: Train the model
Write-Host "`nStep 3: Training Machine Learning Model..." -ForegroundColor Yellow
python model/train_model.py --source csv --file "data/sample_clean_data.csv"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ Model training failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✓ Model trained successfully!" -ForegroundColor Green

# Step 4: Instructions to start services
Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "Setup Complete! Ready to Run" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application, open TWO separate terminals:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Terminal 1 (Backend API):" -ForegroundColor Green
Write-Host "  cd 'C:\Users\singh\OneDrive\Desktop\hackthone 4'" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python backend/app.py" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 2 (Dashboard):" -ForegroundColor Green
Write-Host "  cd 'C:\Users\singh\OneDrive\Desktop\hackthone 4'" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python -m streamlit run dashboard/app.py" -ForegroundColor White
Write-Host ""
Write-Host "The dashboard will open automatically in your browser at: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
