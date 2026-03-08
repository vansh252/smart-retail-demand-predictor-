"""
Database Connection Module for Smart Retail Demand Prediction System
"""

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("Warning: mysql-connector-python not installed. Database features will be unavailable.")
    print("You can still use Excel/CSV files for data input.")
    
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Handles database connections and operations"""
    
    def __init__(self):
        """Initialize database connection parameters"""
        if not MYSQL_AVAILABLE:
            print("MySQL connector not available. Please install: pip install mysql-connector-python")
            print("Or use Excel/CSV files instead.")
            
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '3306')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'retail_demand_db')
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL database"""
        if not MYSQL_AVAILABLE:
            print("Error: MySQL connector not available")
            return False
            
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print(f"Successfully connected to {self.database}")
                return True
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print(f"Query executed successfully: {cursor.rowcount} rows affected")
            cursor.close()
            return True
        except Exception as e:
            print(f"Error executing query: {e}")
            return False
    
    def fetch_data(self, query, params=None):
        """Fetch data from database and return as DataFrame"""
        try:
            if params:
                df = pd.read_sql(query, self.connection, params=params)
            else:
                df = pd.read_sql(query, self.connection)
            print(f"Fetched {len(df)} rows")
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_all_sales_data(self):
        """Retrieve all sales data"""
        query = "SELECT * FROM sales_data"
        return self.fetch_data(query)
    
    def get_sales_by_date_range(self, start_date, end_date):
        """Retrieve sales data within a date range"""
        query = "SELECT * FROM sales_data WHERE sale_date BETWEEN %s AND %s"
        return self.fetch_data(query, params=(start_date, end_date))
    
    def insert_sale(self, product_id, sale_date, region, category, quantity_sold, price, discount):
        """Insert a new sale record"""
        query = """
        INSERT INTO sales_data (product_id, sale_date, region, category, quantity_sold, price, discount)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (product_id, sale_date, region, category, quantity_sold, price, discount)
        return self.execute_query(query, params)


# Example usage
if __name__ == "__main__":
    # Create database connection
    db = DatabaseConnection()
    
    if db.connect():
        # Fetch all sales data
        sales_df = db.get_all_sales_data()
        if sales_df is not None:
            print("\nSales Data:")
            print(sales_df.head())
            print(f"\nTotal records: {len(sales_df)}")
        
        # Close connection
        db.disconnect()
