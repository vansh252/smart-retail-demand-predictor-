# Smart Retail Demand Prediction System - Quick Start
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Smart Retail Demand Prediction System" -ForegroundColor Cyan
Write-Host "Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create sample data
Write-Host "Step 1: Creating Sample Data..." -ForegroundColor Yellow
Write-Host ""

$processExcel = @"
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))
from process_excel import create_sample_excel_with_issues, process_excel_file

print('Creating sample messy data...')
messy_file = create_sample_excel_with_issues()
print('\nProcessing the file...')
cleaned_df = process_excel_file(messy_file)

if cleaned_df is not None:
    print('\n✓ Sample data created and cleaned successfully!')
else:
    print('\n✗ Failed to process data')
    sys.exit(1)
"@

$processExcel | python

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to create sample data" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Find the latest cleaned file
Write-Host "Step 2: Finding Latest Cleaned Data..." -ForegroundColor Yellow

$cleanedFiles = Get-ChildItem -Path "data\cleaned_data_*.csv" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending

if ($cleanedFiles.Count -eq 0) {
    Write-Host "✗ No cleaned data file found!" -ForegroundColor Red
    Write-Host "Please run: python model\process_excel.py" -ForegroundColor Yellow
    exit 1
}

$latestFile = $cleanedFiles[0].Name
Write-Host "✓ Found: $latestFile" -ForegroundColor Green
Write-Host ""

# Step 3: Train model
Write-Host "Step 3: Training Machine Learning Model..." -ForegroundColor Yellow
Write-Host ""

python model\train_model.py --source csv --file "data\$latestFile"

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Model training failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! ✓" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open Terminal 1 and run:" -ForegroundColor White
Write-Host "   python backend\app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Open Terminal 2 and run:" -ForegroundColor White
Write-Host "   streamlit run dashboard\app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Dashboard will open at: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
