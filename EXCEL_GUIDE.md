# Excel Data Processing Guide
# Smart Retail Demand Prediction System

## 📊 Excel File Support

The system now fully supports Excel files (.xlsx, .xls) with comprehensive data validation and cleaning capabilities. This provides hands-on experience with real-world data quality issues.

## 🎯 What You'll Learn

By using Excel files, you'll experience:
- **Data Validation** - Schema checking, data type validation
- **Data Cleaning** - Handling missing values, outliers, inconsistencies
- **Format Standardization** - Fixing case, spaces, date formats
- **Quality Reporting** - Detailed reports of issues found and fixed
- **Error Handling** - Managing incomplete or incorrect data

## 📁 Excel File Requirements

### Required Columns

Your Excel file must contain these columns (case-insensitive):

| Column | Type | Valid Values | Description |
|--------|------|--------------|-------------|
| product_id | Text | P001, P002, etc. | Product identifier |
| sale_date | Date | YYYY-MM-DD | Date of sale |
| region | Text | North, South, East, West | Sales region |
| category | Text | Electronics, Clothing, Furniture | Product category |
| quantity_sold | Number | Positive integers | Units sold |
| price | Number | Positive decimals | Product price ($) |
| discount | Number | 0-100 | Discount percentage |

### Column Names
- Can be in any case (PRODUCT_ID, product_id, Product_Id all work)
- Extra spaces will be automatically trimmed
- Extra columns will be ignored

## 🚀 Getting Started

### Option 1: Use the Template

Create a clean template to fill in:

```bash
python model/process_excel.py
# Choose option 3: Create clean Excel template
```

This creates `data/sales_data_template.xlsx` with the correct format.

### Option 2: Use Sample Messy Data (Learn Data Cleaning)

Generate sample data with intentional issues:

```bash
python model/process_excel.py
# Choose option 2: Create and process sample messy data
```

This demonstrates how the system handles:
- ✗ Inconsistent date formats
- ✗ Mixed case values
- ✗ Invalid categories
- ✗ Negative values
- ✗ Missing data
- ✗ Duplicate records
- ✗ Outliers

### Option 3: Process Your Own File

```bash
python model/process_excel.py
# Choose option 1: Process your own Excel file
# Enter the full path to your file
```

## 📋 Step-by-Step Process

### 1. Prepare Your Excel File

Create an Excel file with your sales data. Don't worry about perfect formatting - the system will handle:
- Date format inconsistencies
- Case variations (north vs North vs NORTH)
- Extra spaces
- Missing values
- Invalid entries

### 2. Process the Excel File

```bash
# Interactive mode
python model/process_excel.py

# Direct processing
python model/process_excel.py path/to/your/file.xlsx
```

### 3. Review the Validation Report

The system performs:

**Step 1: Loading**
- Reads Excel file
- Detects columns
- Reports file info

**Step 2: Schema Validation**
- Checks required columns
- Validates column names
- Identifies extra columns

**Step 3: Data Type Validation**
- Validates dates
- Checks numeric fields
- Verifies categorical values
- Identifies format issues

**Step 4: Duplicate Check**
- Finds complete duplicates
- Detects partial duplicates

**Step 5: Data Cleaning**
- Fixes column names
- Handles missing values
- Converts data types
- Removes invalid records
- Standardizes categories
- Caps outliers

### 4. Review Outputs

The system generates:

1. **Cleaned Data**: `data/cleaned_data_TIMESTAMP.csv`
   - Ready for machine learning
   - All issues resolved
   - Standardized format

2. **Quality Report**: `data/data_quality_report.txt`
   - Detailed validation results
   - Cleaning actions taken
   - Data statistics
   - Before/after comparison

### 5. Train Model with Clean Data

```bash
# Train using the cleaned data
python model/train_model.py --source csv --file data/cleaned_data_TIMESTAMP.csv
```

Or continue using the database:
```bash
python model/train_model.py
```

## 🔍 Data Validation Details

### Date Validation

**Accepts:**
- 2024-01-15
- 2024/01/15
- 01-15-2024
- Excel date numbers

**Rejects:**
- Future dates
- Invalid formats
- Non-date text

**Action:** Invalid dates are removed

### Numeric Validation (price, discount)

**Checks:**
- Can be converted to number
- Not negative (price)
- Within valid range

**Actions:**
- Fills missing with median
- Removes negative prices
- Caps discount at 100%
- Sets negative discounts to 0

### Integer Validation (quantity_sold)

**Checks:**
- Positive integers only
- No decimals
- No zero values

**Actions:**
- Fills missing with median
- Removes zero/negative
- Rounds decimals

### Categorical Validation

**Categories:**
- Electronics
- Clothing  
- Furniture

**Regions:**
- North
- South
- East
- West

**Actions:**
- Standardizes case (Title Case)
- Trims spaces
- Attempts fuzzy matching
- Removes invalid values

### Product ID Validation

**Expected Format:** P001, P002, P003...

**Actions:**
- Converts to uppercase
- Trims spaces
- Accepts variations

## 📊 Example: Processing Messy Data

### Input Excel (with issues):

```
Product_ID  | Sale_Date    | Region  | Category   | Quantity_Sold | Price     | Discount
P001        | 2024-01-15   | North   | Electronics| 50            | 299.99    | 10
P002        | 2024/01/16   | south   | Cloth      | 120           | 49.99     | 5
P003        | invalid      | Unknown | electronics| -30           | expensive | 150
  P004      | 2024-01-18   | WEST    | Furniture  |               | 599.99    | -5
```

### Output (cleaned):

```
product_id | sale_date  | region | category    | quantity_sold | price  | discount
P001       | 2024-01-15 | North  | Electronics | 50            | 299.99 | 10.0
P002       | 2024-01-16 | South  | Clothing    | 120           | 49.99  | 5.0
P004       | 2024-01-18 | West   | Furniture   | 85            | 599.99 | 0.0
```

**Cleaning Actions:**
- Row 3: Removed (invalid date, invalid category, negative quantity, non-numeric price)
- Row 4: Quantity filled with median (85), discount set to 0
- All: Standardized case, trimmed spaces

### Validation Report Shows:

```
VALIDATION RESULTS:
- Found 4 rows
- Missing values: 1 (quantity_sold)
- Invalid dates: 1
- Invalid categories: 2
- Non-numeric values: 1 (price)
- Negative values: 2 (quantity_sold, discount)
- Excessive discount: 1 (150%)

CLEANING ACTIONS:
- Standardized column names
- Removed 1 row with invalid date
- Filled 1 missing quantity_sold
- Standardized 4 categorical values
- Capped 1 discount over 100%
- Set 1 negative discount to 0
- Removed 1 row with negative quantity

FINAL RESULT:
- Initial: 4 rows
- Final: 3 rows  
- Quality: 75%
```

## 💡 Best Practices

### For Learning:
1. Start with sample messy data
2. Review the detailed validation report
3. Understand each cleaning action
4. Try different types of errors

### For Production:
1. Use the template as a starting point
2. Ensure dates are in YYYY-MM-DD format
3. Use consistent capitalization
4. Validate data before upload
5. Review the quality report

### Common Issues & Solutions:

| Issue | Solution |
|-------|----------|
| "Missing required columns" | Check column names match exactly |
| "Invalid date format" | Use YYYY-MM-DD or let system convert |
| "Invalid category" | Use: Electronics, Clothing, Furniture only |
| "Invalid region" | Use: North, South, East, West only |
| "Negative values" | Ensure quantity > 0, price > 0 |
| "File not found" | Use full path or check file location |

## 🎓 Learning Exercises

### Exercise 1: Perfect Data
1. Use the clean template
2. Add 10-20 records
3. Process and verify 100% quality score

### Exercise 2: Messy Data
1. Generate sample messy data
2. Review validation report
3. Understand each issue found
4. See how system fixes each one

### Exercise 3: Your Own Data
1. Export your data to Excel
2. Process through validation
3. Review quality score
4. Fix issues in original data
5. Reprocess and compare

### Exercise 4: Edge Cases
Create data with:
- Future dates (should be removed)
- 150% discount (should be capped)
- Zero quantity (should be removed)
- Invalid category "Books" (should be removed)
- Missing price (should be filled with median)

## 📈 Integration with ML Pipeline

### Complete Workflow:

```bash
# 1. Create or prepare Excel file
# data/my_sales_data.xlsx

# 2. Process and clean
python model/process_excel.py

# 3. Train model with cleaned data
python model/train_model.py --source csv --file data/cleaned_data_*.csv

# 4. Start API with new model
python backend/app.py

# 5. Use dashboard
streamlit run dashboard/app.py
```

### Or use interactive mode:

```bash
python model/process_excel.py
# Follow prompts to process, clean, and prepare data
```

## 🔧 Advanced Options

### Command Line Processing:

```bash
# Process specific Excel file
python model/process_excel.py your_file.xlsx

# Train directly from Excel (with validation)
python model/train_model.py --source excel --file data/sales_data.xlsx

# Train from CSV (already cleaned)
python model/train_model.py --source csv --file data/cleaned_data.csv
```

### Customization:

Edit `model/data_validator.py` to:
- Add custom validation rules
- Change acceptable value ranges
- Add new categories/regions
- Customize cleaning logic

## 📞 Troubleshooting

### "openpyxl not found"
```bash
pip install openpyxl
```

### "No module named 'xlrd'"
```bash
pip install xlrd
```

### "Cannot process file"
- Check file extension (.xlsx or .xls)
- Ensure file is not open in Excel
- Verify file is not corrupted

### "All rows removed during cleaning"
- Check if data matches expected format
- Review validation report for issues
- Ensure categories and regions are valid

## 🎯 Summary

Excel support provides:
- ✅ Flexible data input
- ✅ Comprehensive validation
- ✅ Automatic cleaning
- ✅ Detailed reporting
- ✅ Learning experience
- ✅ Production-ready pipeline

This gives you hands-on experience with real-world data quality challenges and solutions!

---

**For more information, see README.md and QUICK_REFERENCE.md**
