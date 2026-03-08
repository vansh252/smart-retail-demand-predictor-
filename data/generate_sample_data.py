"""
Generate Sample Sales Data for Testing
Creates realistic synthetic sales data and inserts into database
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add database directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from db_connection import DatabaseConnection


def generate_sample_data(num_records=100):
    """
    Generate synthetic sales data
    
    Args:
        num_records: Number of records to generate
        
    Returns:
        List of tuples with sales data
    """
    print(f"Generating {num_records} sample records...")
    
    # Configuration
    products = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010']
    categories = ['Electronics', 'Clothing', 'Furniture']
    regions = ['North', 'South', 'East', 'West']
    
    # Price ranges by category
    price_ranges = {
        'Electronics': (99.99, 999.99),
        'Clothing': (19.99, 149.99),
        'Furniture': (299.99, 1999.99)
    }
    
    # Generate data
    sales_data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_records):
        # Random date within last year
        days_offset = random.randint(0, 365)
        sale_date = start_date + timedelta(days=days_offset)
        
        # Random product and category
        product_id = random.choice(products)
        category = random.choice(categories)
        region = random.choice(regions)
        
        # Price based on category
        min_price, max_price = price_ranges[category]
        price = round(random.uniform(min_price, max_price), 2)
        
        # Discount (more likely to be 0-20%)
        discount = round(random.choices(
            [0, 5, 10, 15, 20, 25, 30],
            weights=[30, 25, 20, 15, 7, 2, 1]
        )[0], 2)
        
        # Quantity sold (influenced by price and discount)
        base_quantity = random.randint(20, 200)
        
        # Higher discount = more quantity
        discount_factor = 1 + (discount / 100)
        
        # Lower price = more quantity
        price_factor = 1 / (price / 100)
        
        quantity_sold = int(base_quantity * discount_factor * min(price_factor, 2))
        quantity_sold = max(1, min(quantity_sold, 500))  # Between 1 and 500
        
        # Add seasonal variation (more sales in certain months)
        month = sale_date.month
        if month in [11, 12]:  # Holiday season
            quantity_sold = int(quantity_sold * 1.5)
        elif month in [6, 7]:  # Summer
            quantity_sold = int(quantity_sold * 1.2)
        
        sales_data.append((
            product_id,
            sale_date.strftime('%Y-%m-%d'),
            region,
            category,
            quantity_sold,
            price,
            discount
        ))
    
    print(f"✓ Generated {len(sales_data)} records")
    return sales_data


def insert_sample_data(sales_data):
    """
    Insert generated data into database
    
    Args:
        sales_data: List of tuples with sales data
    """
    print("\nConnecting to database...")
    db = DatabaseConnection()
    
    if not db.connect():
        print("✗ Failed to connect to database")
        return False
    
    print("✓ Connected to database")
    print("\nInserting data...")
    
    query = """
    INSERT INTO sales_data (product_id, sale_date, region, category, quantity_sold, price, discount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    success_count = 0
    error_count = 0
    
    for record in sales_data:
        if db.execute_query(query, record):
            success_count += 1
        else:
            error_count += 1
        
        # Progress indicator
        if (success_count + error_count) % 10 == 0:
            print(f"Progress: {success_count + error_count}/{len(sales_data)}")
    
    db.disconnect()
    
    print("\n" + "=" * 60)
    print("Data Generation Complete")
    print("=" * 60)
    print(f"Successfully inserted: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Total: {len(sales_data)}")
    
    return True


def main():
    """Main function"""
    print("=" * 60)
    print("Sample Data Generator")
    print("Smart Retail Demand Prediction System")
    print("=" * 60)
    print()
    
    # Get number of records from user
    try:
        num_records = input("Enter number of records to generate (default: 100): ")
        num_records = int(num_records) if num_records else 100
        
        if num_records < 1 or num_records > 10000:
            print("Please enter a number between 1 and 10000")
            return
    except ValueError:
        print("Invalid input. Using default: 100")
        num_records = 100
    
    print()
    
    # Generate data
    sales_data = generate_sample_data(num_records)
    
    # Confirm before inserting
    confirm = input("\nInsert data into database? (y/n): ")
    
    if confirm.lower() == 'y':
        insert_sample_data(sales_data)
        print("\n✓ Done! You may now retrain the model with new data.")
    else:
        print("Cancelled.")


if __name__ == "__main__":
    main()
