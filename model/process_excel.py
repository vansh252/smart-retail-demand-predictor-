"""
Excel Data Processor - Process Excel files with comprehensive validation
Demonstrates complete data quality pipeline
"""

import pandas as pd
import sys
import os
from datetime import datetime

# Add paths
sys.path.append(os.path.dirname(__file__))
from data_validator import DataValidator
from data_processing import DataProcessor


def process_excel_file(excel_path, save_cleaned=True, save_report=True):
    """
    Process an Excel file with full validation and cleaning
    
    Args:
        excel_path: Path to Excel file
        save_cleaned: Save cleaned data to CSV
        save_report: Save validation report
        
    Returns:
        Cleaned DataFrame or None
    """
    print("=" * 80)
    print("EXCEL DATA PROCESSOR")
    print("Smart Retail Demand Prediction System")
    print("=" * 80)
    print(f"\nProcessing file: {excel_path}\n")
    
    # Initialize processor with Excel source
    processor = DataProcessor(data_source='excel', use_validation=True)
    
    # Process the file
    if not processor.process_pipeline(filepath=excel_path):
        print("\n✗ Processing failed")
        return None
    
    # Get cleaned and processed data
    cleaned_data = processor.get_processed_dataframe()
    
    if cleaned_data is None:
        print("\n✗ No data available")
        return None
    
    # Save cleaned data
    if save_cleaned:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_csv = os.path.join(output_dir, f'cleaned_data_{timestamp}.csv')
        
        cleaned_data.to_csv(output_csv, index=False)
        print(f"\n✓ Cleaned data saved to: {output_csv}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\nFinal Dataset:")
    print(f"  Rows: {len(cleaned_data)}")
    print(f"  Columns: {len(cleaned_data.columns)}")
    print(f"\nColumns: {', '.join(cleaned_data.columns)}")
    
    print(f"\n Category Distribution:")
    print(cleaned_data['category'].value_counts().to_string())
    
    print(f"\nRegion Distribution:")
    print(cleaned_data['region'].value_counts().to_string())
    
    print(f"\nPrice Statistics:")
    print(f"  Min: ${cleaned_data['price'].min():.2f}")
    print(f"  Max: ${cleaned_data['price'].max():.2f}")
    print(f"  Mean: ${cleaned_data['price'].mean():.2f}")
    print(f"  Median: ${cleaned_data['price'].median():.2f}")
    
    print(f"\nQuantity Sold Statistics:")
    print(f"  Min: {cleaned_data['quantity_sold'].min()}")
    print(f"  Max: {cleaned_data['quantity_sold'].max()}")
    print(f"  Mean: {cleaned_data['quantity_sold'].mean():.1f}")
    print(f"  Total: {cleaned_data['quantity_sold'].sum()}")
    
    return cleaned_data


def create_sample_excel_with_issues():
    """
    Create a sample Excel file with intentional data quality issues
    This demonstrates the validator's capabilities
    """
    print("\n" + "=" * 80)
    print("Creating Sample Excel File with Data Quality Issues")
    print("=" * 80)
    
    # Create messy data with common issues
    data = {
        'Product_ID': ['P001', 'P002', 'P003', 'P004', ' P005', 'P001', '  P007  ', 'P008', None, 'P010'],
        'Sale_Date': ['2024-01-15', '2024-01-16', '2024/01/17', '01-18-2024', '2024-01-19', 
                      '2024-01-15', 'invalid', '2024-02-20', '2024-02-21', '2030-12-31'],
        'Region ': ['North', 'South', 'east', 'West', 'NORTH', 'North', 'Unknown', 'East', 'South', 'West'],
        'Category': ['Electronics', 'Clothing', 'electronics', 'Furniture', 'Cloth', 
                    'Electronics', 'Books', 'Furniture', 'Clothing', 'Electronics'],
        'Quantity_Sold': [50, 120, 75.5, -30, 200, 50, 0, 150, None, 80],
        'Price': [299.99, 49.99, 199.99, 599.99, 29.99, 299.99, 'expensive', -50, 399.99, 149.99],
        'Discount': [10, 5, 15, 20, 0, 10, 150, -5, None, 8]
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    excel_path = os.path.join(output_dir, 'sample_messy_data.xlsx')
    df.to_excel(excel_path, index=False, engine='openpyxl')
    
    print(f"\n✓ Created sample Excel file: {excel_path}")
    print("\nIntentional issues included:")
    print("  ✗ Inconsistent date formats")
    print("  ✗ Leading/trailing spaces in values")
    print("  ✗ Inconsistent capitalization")
    print("  ✗ Invalid categories and regions")
    print("  ✗ Negative and zero quantities")
    print("  ✗ Non-numeric price values")
    print("  ✗ Discounts over 100% and negative")
    print("  ✗ Missing values")
    print("  ✗ Duplicate records")
    print("  ✗ Future dates")
    print("  ✗ Extra spaces in column names")
    print("")
    
    return excel_path


def create_clean_template():
    """Create a clean Excel template for users"""
    print("\n" + "= " * 80)
    print("Creating Clean Excel Template")
    print("=" * 80)
    
    # Create template with sample data
    data = {
        'product_id': ['P001', 'P002', 'P003'],
        'sale_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'region': ['North', 'South', 'East'],
        'category': ['Electronics', 'Clothing', 'Furniture'],
        'quantity_sold': [50, 120, 30],
        'price': [299.99, 49.99, 599.99],
        'discount': [10.0, 5.0, 20.0]
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    template_path = os.path.join(output_dir, 'sales_data_template.xlsx')
    df.to_excel(template_path, index=False, engine='openpyxl')
    
    print(f"\n✓ Created template: {template_path}")
    print("\nTemplate Guidelines:")
    print("  • product_id: Alphanumeric (e.g., P001, P002)")
    print("  • sale_date: YYYY-MM-DD format")
    print("  • region: North, South, East, or West")
    print("  • category: Electronics, Clothing, or Furniture")
    print("  • quantity_sold: Positive integer")
    print("  • price: Positive number (decimal allowed)")
    print("  • discount: 0-100 (percentage)")
    print("")
    
    return template_path


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("EXCEL DATA PROCESSOR - Interactive Mode")
    print("=" * 80)
    
    while True:
        print("\nOptions:")
        print("1. Process your own Excel file")
        print("2. Create and process sample messy data (demonstration)")
        print("3. Create clean Excel template")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            excel_path = input("\nEnter path to your Excel file: ").strip()
            
            if not os.path.exists(excel_path):
                print(f"\n✗ File not found: {excel_path}")
                continue
            
            process_excel_file(excel_path)
            
        elif choice == '2':
            # Create sample with issues
            messy_file = create_sample_excel_with_issues()
            
            proceed = input("\nProcess this messy file now? (y/n): ").lower()
            if proceed == 'y':
                process_excel_file(messy_file)
            
        elif choice == '3':
            create_clean_template()
            
        elif choice == '4':
            print("\nGoodbye!")
            break
            
        else:
            print("\n✗ Invalid choice. Please enter 1-4.")
        
        # Ask to continue
        cont = input("\nPerform another operation? (y/n): ").lower()
        if cont != 'y':
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    # Check if file path provided as argument
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        process_excel_file(excel_file)
    else:
        main()
