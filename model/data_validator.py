"""
Advanced Data Validation and Cleaning Module
Comprehensive data quality checks and cleaning for retail sales data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
import os


class DataValidator:
    """
    Comprehensive data validation and cleaning for sales data
    Provides detailed reports and handles various data quality issues
    """
    
    def __init__(self, verbose=True):
        """
        Initialize validator
        
        Args:
            verbose: If True, print detailed logs
        """
        self.verbose = verbose
        self.validation_report = []
        self.cleaning_report = []
        self.data = None
        self.original_data = None
        
        # Expected schema
        self.expected_columns = {
            'product_id': 'object',
            'sale_date': 'datetime64',
            'region': 'object',
            'category': 'object',
            'quantity_sold': 'int',
            'price': 'float',
            'discount': 'float'
        }
        
        # Valid values
        self.valid_categories = ['Electronics', 'Clothing', 'Furniture']
        self.valid_regions = ['North', 'South', 'East', 'West']
    
    def log(self, message, level='INFO'):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        if level == 'VALIDATION':
            self.validation_report.append(log_entry)
        elif level == 'CLEANING':
            self.cleaning_report.append(log_entry)
        
        if self.verbose:
            print(log_entry)
    
    def load_excel_file(self, filepath):
        """
        Load data from Excel file with error handling
        
        Args:
            filepath: Path to Excel file (.xlsx or .xls)
            
        Returns:
            DataFrame or None
        """
        self.log("=" * 80)
        self.log("STEP 1: LOADING EXCEL FILE")
        self.log("=" * 80)
        
        if not os.path.exists(filepath):
            self.log(f"File not found: {filepath}", 'ERROR')
            return None
        
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension not in ['.xlsx', '.xls']:
            self.log(f"Unsupported file format: {file_extension}", 'ERROR')
            self.log("Please provide .xlsx or .xls file", 'ERROR')
            return None
        
        try:
            self.log(f"Reading file: {filepath}")
            
            # Try different engines
            if file_extension == '.xlsx':
                df = pd.read_excel(filepath, engine='openpyxl')
            else:
                df = pd.read_excel(filepath, engine='xlrd')
            
            self.log(f"✓ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            self.log(f"Columns found: {', '.join(df.columns)}")
            
            self.data = df.copy()
            self.original_data = df.copy()
            
            return df
            
        except Exception as e:
            self.log(f"Error loading Excel file: {e}", 'ERROR')
            return None
    
    def validate_schema(self):
        """Validate column names and data types"""
        self.log("\n" + "=" * 80)
        self.log("STEP 2: SCHEMA VALIDATION")
        self.log("=" * 80)
        
        if self.data is None:
            self.log("No data to validate", 'ERROR')
            return False
        
        df = self.data
        issues_found = 0
        
        # Check for required columns
        self.log("\n2.1 Checking Required Columns:")
        missing_columns = []
        
        for col in self.expected_columns.keys():
            if col not in df.columns:
                missing_columns.append(col)
                issues_found += 1
        
        if missing_columns:
            self.log(f"✗ Missing columns: {', '.join(missing_columns)}", 'VALIDATION')
        else:
            self.log("✓ All required columns present", 'VALIDATION')
        
        # Check for extra columns
        extra_columns = [col for col in df.columns if col not in self.expected_columns.keys()]
        if extra_columns:
            self.log(f"⚠ Extra columns found (will be ignored): {', '.join(extra_columns)}", 'VALIDATION')
        
        # Check column names (case sensitivity, spaces)
        self.log("\n2.2 Checking Column Name Format:")
        for col in df.columns:
            if col != col.strip():
                self.log(f"⚠ Column has leading/trailing spaces: '{col}'", 'VALIDATION')
                issues_found += 1
            
            if col != col.lower():
                self.log(f"⚠ Column is not lowercase: '{col}'", 'VALIDATION')
        
        return issues_found == 0
    
    def validate_data_types(self):
        """Validate and report data type issues"""
        self.log("\n" + "=" * 80)
        self.log("STEP 3: DATA TYPE VALIDATION")
        self.log("=" * 80)
        
        if self.data is None:
            return False
        
        df = self.data
        
        for col in df.columns:
            if col not in self.expected_columns:
                continue
            
            self.log(f"\n3.{list(self.expected_columns.keys()).index(col) + 1} Validating '{col}':")
            self.log(f"Current dtype: {df[col].dtype}")
            self.log(f"Expected type: {self.expected_columns[col]}")
            
            # Check for null values
            null_count = df[col].isnull().sum()
            if null_count > 0:
                null_pct = (null_count / len(df)) * 100
                self.log(f"⚠ Missing values: {null_count} ({null_pct:.2f}%)", 'VALIDATION')
            else:
                self.log(f"✓ No missing values", 'VALIDATION')
            
            # Type-specific validation
            if col == 'sale_date':
                self._validate_dates(df[col])
            elif col in ['price', 'discount']:
                self._validate_numeric(df[col], col)
            elif col == 'quantity_sold':
                self._validate_integer(df[col], col)
            elif col in ['category', 'region']:
                self._validate_categorical(df[col], col)
            elif col == 'product_id':
                self._validate_product_id(df[col])
        
        return True
    
    def _validate_dates(self, series):
        """Validate date column"""
        try:
            # Try to convert to datetime
            converted = pd.to_datetime(series, errors='coerce')
            invalid_dates = converted.isnull().sum() - series.isnull().sum()
            
            if invalid_dates > 0:
                self.log(f"⚠ Invalid date format: {invalid_dates} rows", 'VALIDATION')
            else:
                self.log(f"✓ All dates valid", 'VALIDATION')
            
            # Check date range
            valid_dates = converted.dropna()
            if len(valid_dates) > 0:
                min_date = valid_dates.min()
                max_date = valid_dates.max()
                self.log(f"Date range: {min_date.date()} to {max_date.date()}", 'VALIDATION')
                
                # Check for future dates
                today = pd.Timestamp.now()
                future_dates = (valid_dates > today).sum()
                if future_dates > 0:
                    self.log(f"⚠ Future dates found: {future_dates} rows", 'VALIDATION')
                
        except Exception as e:
            self.log(f"✗ Date validation error: {e}", 'VALIDATION')
    
    def _validate_numeric(self, series, col_name):
        """Validate numeric columns"""
        # Check if can be converted to numeric
        numeric_series = pd.to_numeric(series, errors='coerce')
        non_numeric = numeric_series.isnull().sum() - series.isnull().sum()
        
        if non_numeric > 0:
            self.log(f"⚠ Non-numeric values: {non_numeric} rows", 'VALIDATION')
        else:
            self.log(f"✓ All values numeric", 'VALIDATION')
        
        # Check for negative values
        valid_values = numeric_series.dropna()
        if len(valid_values) > 0:
            negative = (valid_values < 0).sum()
            if negative > 0:
                self.log(f"⚠ Negative values: {negative} rows", 'VALIDATION')
            
            # Statistics
            self.log(f"Range: {valid_values.min():.2f} to {valid_values.max():.2f}", 'VALIDATION')
            self.log(f"Mean: {valid_values.mean():.2f}, Median: {valid_values.median():.2f}", 'VALIDATION')
            
            # Check for outliers using IQR
            Q1 = valid_values.quantile(0.25)
            Q3 = valid_values.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((valid_values < Q1 - 3*IQR) | (valid_values > Q3 + 3*IQR)).sum()
            if outliers > 0:
                self.log(f"⚠ Potential outliers (3×IQR): {outliers} rows", 'VALIDATION')
    
    def _validate_integer(self, series, col_name):
        """Validate integer columns"""
        # Check if can be converted to integer
        try:
            int_series = pd.to_numeric(series, errors='coerce')
            non_numeric = int_series.isnull().sum() - series.isnull().sum()
            
            if non_numeric > 0:
                self.log(f"⚠ Non-numeric values: {non_numeric} rows", 'VALIDATION')
            
            valid_values = int_series.dropna()
            if len(valid_values) > 0:
                # Check for decimals
                has_decimals = (valid_values != valid_values.astype(int)).sum()
                if has_decimals > 0:
                    self.log(f"⚠ Decimal values (expected integers): {has_decimals} rows", 'VALIDATION')
                
                # Check for negative or zero
                invalid = (valid_values <= 0).sum()
                if invalid > 0:
                    self.log(f"⚠ Zero or negative values: {invalid} rows", 'VALIDATION')
                else:
                    self.log(f"✓ All values positive integers", 'VALIDATION')
                
                self.log(f"Range: {int(valid_values.min())} to {int(valid_values.max())}", 'VALIDATION')
                
        except Exception as e:
            self.log(f"✗ Integer validation error: {e}", 'VALIDATION')
    
    def _validate_categorical(self, series, col_name):
        """Validate categorical columns"""
        valid_values = self.valid_categories if col_name == 'category' else self.valid_regions
        
        # Get unique values
        unique_vals = series.dropna().unique()
        self.log(f"Unique values: {', '.join(map(str, unique_vals))}", 'VALIDATION')
        
        # Check for invalid categories
        invalid = [val for val in unique_vals if val not in valid_values]
        if invalid:
            self.log(f"⚠ Invalid values: {', '.join(invalid)}", 'VALIDATION')
            self.log(f"Valid values: {', '.join(valid_values)}", 'VALIDATION')
        else:
            self.log(f"✓ All values valid", 'VALIDATION')
        
        # Check for case sensitivity issues
        for val in unique_vals:
            if isinstance(val, str):
                if val != val.strip():
                    self.log(f"⚠ Value has spaces: '{val}'", 'VALIDATION')
    
    def _validate_product_id(self, series):
        """Validate product ID column"""
        unique_count = series.nunique()
        self.log(f"Unique product IDs: {unique_count}", 'VALIDATION')
        
        # Check format (expecting P001, P002, etc.)
        valid_values = series.dropna()
        pattern = re.compile(r'^P\d{3,}$')
        
        invalid_format = 0
        for val in valid_values:
            if not pattern.match(str(val)):
                invalid_format += 1
        
        if invalid_format > 0:
            self.log(f"⚠ Non-standard format: {invalid_format} rows", 'VALIDATION')
            self.log(f"Expected format: P001, P002, etc.", 'VALIDATION')
    
    def check_duplicates(self):
        """Check for duplicate records"""
        self.log("\n" + "=" * 80)
        self.log("STEP 4: DUPLICATE CHECK")
        self.log("=" * 80)
        
        if self.data is None:
            return
        
        df = self.data
        
        # Check complete duplicates
        total_duplicates = df.duplicated().sum()
        if total_duplicates > 0:
            self.log(f"⚠ Complete duplicate rows: {total_duplicates}", 'VALIDATION')
        else:
            self.log(f"✓ No complete duplicates found", 'VALIDATION')
        
        # Check partial duplicates (same product_id and date)
        if 'product_id' in df.columns and 'sale_date' in df.columns:
            partial_dupes = df.duplicated(subset=['product_id', 'sale_date'], keep=False).sum()
            if partial_dupes > 0:
                self.log(f"⚠ Duplicate product_id + date combinations: {partial_dupes}", 'VALIDATION')
    
    def clean_data(self):
        """
        Comprehensive data cleaning pipeline
        Applies fixes for all identified issues
        """
        self.log("\n" + "=" * 80)
        self.log("STEP 5: DATA CLEANING")
        self.log("=" * 80)
        
        if self.data is None:
            return None
        
        df = self.data.copy()
        initial_rows = len(df)
        
        # 5.1 Clean column names
        self.log("\n5.1 Cleaning Column Names:")
        df.columns = df.columns.str.strip().str.lower()
        self.log("✓ Trimmed spaces and converted to lowercase", 'CLEANING')
        
        # 5.2 Handle missing columns
        self.log("\n5.2 Handling Missing Required Columns:")
        for col in self.expected_columns.keys():
            if col not in df.columns:
                self.log(f"✗ Cannot proceed: Missing required column '{col}'", 'ERROR')
                return None
        
        # Select only required columns
        df = df[list(self.expected_columns.keys())]
        self.log(f"✓ Selected {len(df.columns)} required columns", 'CLEANING')
        
        # 5.3 Remove complete duplicates
        self.log("\n5.3 Removing Duplicates:")
        duplicates_before = df.duplicated().sum()
        df = df.drop_duplicates()
        duplicates_removed = duplicates_before
        if duplicates_removed > 0:
            self.log(f"✓ Removed {duplicates_removed} duplicate rows", 'CLEANING')
        else:
            self.log(f"✓ No duplicates to remove", 'CLEANING')
        
        # 5.4 Clean and convert dates
        self.log("\n5.4 Cleaning Date Column:")
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
        invalid_dates = df['sale_date'].isnull().sum()
        if invalid_dates > 0:
            self.log(f"⚠ Removing {invalid_dates} rows with invalid dates", 'CLEANING')
            df = df.dropna(subset=['sale_date'])
        self.log(f"✓ Converted to datetime format", 'CLEANING')
        
        # Remove future dates
        today = pd.Timestamp.now()
        future_dates = (df['sale_date'] > today).sum()
        if future_dates > 0:
            self.log(f"⚠ Removing {future_dates} future dated records", 'CLEANING')
            df = df[df['sale_date'] <= today]
        
        # 5.5 Clean numeric columns
        self.log("\n5.5 Cleaning Numeric Columns:")
        
        # Price
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        invalid_price = df['price'].isnull().sum()
        df['price'].fillna(df['price'].median(), inplace=True)
        self.log(f"✓ Converted price to numeric (filled {invalid_price} missing)", 'CLEANING')
        
        # Remove negative prices
        negative_price = (df['price'] < 0).sum()
        if negative_price > 0:
            self.log(f"⚠ Removing {negative_price} rows with negative prices", 'CLEANING')
            df = df[df['price'] >= 0]
        
        # Discount
        df['discount'] = pd.to_numeric(df['discount'], errors='coerce')
        df['discount'].fillna(0, inplace=True)
        self.log(f"✓ Converted discount to numeric (filled missing with 0)", 'CLEANING')
        
        # Cap discount at 100%
        excessive_discount = (df['discount'] > 100).sum()
        if excessive_discount > 0:
            self.log(f"⚠ Capping {excessive_discount} discounts over 100%", 'CLEANING')
            df.loc[df['discount'] > 100, 'discount'] = 100
        
        # Ensure non-negative
        df.loc[df['discount'] < 0, 'discount'] = 0
        
        # Quantity
        df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
        invalid_qty = df['quantity_sold'].isnull().sum()
        df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
        df['quantity_sold'] = df['quantity_sold'].astype(int)
        self.log(f"✓ Converted quantity to integer (filled {invalid_qty} missing)", 'CLEANING')
        
        # Remove zero or negative quantities
        invalid_qty_values = (df['quantity_sold'] <= 0).sum()
        if invalid_qty_values > 0:
            self.log(f"⚠ Removing {invalid_qty_values} rows with invalid quantities", 'CLEANING')
            df = df[df['quantity_sold'] > 0]
        
        # 5.6 Clean categorical columns
        self.log("\n5.6 Cleaning Categorical Columns:")
        
        # Category
        df['category'] = df['category'].str.strip().str.title()
        invalid_category = ~df['category'].isin(self.valid_categories)
        invalid_count = invalid_category.sum()
        if invalid_count > 0:
            # Try to fix common misspellings
            df.loc[df['category'].str.contains('Elect', case=False, na=False), 'category'] = 'Electronics'
            df.loc[df['category'].str.contains('Cloth', case=False, na=False), 'category'] = 'Clothing'
            df.loc[df['category'].str.contains('Furni', case=False, na=False), 'category'] = 'Furniture'
            
            # Remove still invalid
            still_invalid = ~df['category'].isin(self.valid_categories)
            if still_invalid.sum() > 0:
                self.log(f"⚠ Removing {still_invalid.sum()} rows with invalid categories", 'CLEANING')
                df = df[df['category'].isin(self.valid_categories)]
        self.log(f"✓ Standardized categories", 'CLEANING')
        
        # Region
        df['region'] = df['region'].str.strip().str.title()
        invalid_region = ~df['region'].isin(self.valid_regions)
        if invalid_region.sum() > 0:
            self.log(f"⚠ Removing {invalid_region.sum()} rows with invalid regions", 'CLEANING')
            df = df[df['region'].isin(self.valid_regions)]
        self.log(f"✓ Standardized regions", 'CLEANING')
        
        # Product ID
        df['product_id'] = df['product_id'].astype(str).str.strip().str.upper()
        self.log(f"✓ Standardized product IDs", 'CLEANING')
        
        # 5.7 Summary
        final_rows = len(df)
        rows_removed = initial_rows - final_rows
        
        self.log("\n" + "=" * 80)
        self.log("CLEANING SUMMARY")
        self.log("=" * 80)
        self.log(f"Initial rows: {initial_rows}")
        self.log(f"Final rows: {final_rows}")
        self.log(f"Rows removed: {rows_removed} ({(rows_removed/initial_rows)*100:.2f}%)")
        self.log(f"Data quality: {(final_rows/initial_rows)*100:.2f}%")
        
        self.data = df
        return df
    
    def generate_report(self, output_file=None):
        """Generate comprehensive validation and cleaning report"""
        report = []
        report.append("=" * 80)
        report.append("DATA VALIDATION AND CLEANING REPORT")
        report.append("Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        report.append("=" * 80)
        report.append("")
        
        report.append("VALIDATION RESULTS:")
        report.append("-" * 80)
        report.extend(self.validation_report)
        report.append("")
        
        report.append("CLEANING ACTIONS:")
        report.append("-" * 80)
        report.extend(self.cleaning_report)
        report.append("")
        
        if self.data is not None:
            report.append("FINAL DATA STATISTICS:")
            report.append("-" * 80)
            report.append(f"Total records: {len(self.data)}")
            report.append(f"Columns: {', '.join(self.data.columns)}")
            report.append("")
            report.append("Summary Statistics:")
            report.append(str(self.data.describe()))
            report.append("")
            report.append("Category Distribution:")
            report.append(str(self.data['category'].value_counts()))
            report.append("")
            report.append("Region Distribution:")
            report.append(str(self.data['region'].value_counts()))
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            self.log(f"\n✓ Report saved to: {output_file}")
        
        return report_text
    
    def get_cleaned_data(self):
        """Return the cleaned DataFrame"""
        return self.data


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("DATA VALIDATOR - Example Usage")
    print("=" * 80)
    print("\nThis module validates and cleans Excel/CSV sales data.")
    print("\nUsage:")
    print("  validator = DataValidator(verbose=True)")
    print("  validator.load_excel_file('your_data.xlsx')")
    print("  validator.validate_schema()")
    print("  validator.validate_data_types()")
    print("  validator.check_duplicates()")
    print("  cleaned_df = validator.clean_data()")
    print("  validator.generate_report('report.txt')")
