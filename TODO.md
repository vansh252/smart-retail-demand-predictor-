# Smart Retail Demand Predictor - Run Project TODO

## Current Status
- [x] Analyzed project structure and files
- [IN PROGRESS] 1. Install dependencies (`pip install -r requirements.txt` running)
- [ ] 2. Train model (`python model/train_model.py --source csv --file data/sample_clean_data.csv`)
- [ ] 3. Start backend API (Terminal 1: `python backend/app.py`)
- [ ] 4. Start dashboard (Terminal 2: `streamlit run dashboard/app.py`)
- [ ] 5. Access dashboard at http://localhost:8501

## Quick Commands (after step 1 completes)
```
python model/train_model.py --source csv --file data/sample_clean_data.csv
python backend/app.py    # Keep running
# New terminal: streamlit run dashboard/app.py
```

**Expected Output after Step 2:**
- `model/demand_model.pkl` created
- Training metrics printed (MAE, R2, feature importance)

**Troubleshooting:**
- If training fails: Check `data/sample_clean_data.csv`
- Backend ready message: "API Server Ready"
- Dashboard opens automatically
