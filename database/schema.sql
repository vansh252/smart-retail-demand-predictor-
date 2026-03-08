-- Smart Retail Demand Prediction System
-- Database Schema

CREATE DATABASE IF NOT EXISTS retail_demand_db;
USE retail_demand_db;

-- Sales Data Table
CREATE TABLE IF NOT EXISTS sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    sale_date DATE NOT NULL,
    region VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity_sold INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(5, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product (product_id),
    INDEX idx_date (sale_date),
    INDEX idx_region (region),
    INDEX idx_category (category)
);

-- Insert sample data for testing
INSERT INTO sales_data (product_id, sale_date, region, category, quantity_sold, price, discount) VALUES
('P001', '2024-01-15', 'North', 'Electronics', 50, 299.99, 10.00),
('P002', '2024-01-16', 'South', 'Clothing', 120, 49.99, 5.00),
('P003', '2024-01-17', 'East', 'Electronics', 75, 199.99, 15.00),
('P004', '2024-01-18', 'West', 'Furniture', 30, 599.99, 20.00),
('P005', '2024-01-19', 'North', 'Clothing', 200, 29.99, 0.00),
('P001', '2024-02-15', 'North', 'Electronics', 60, 299.99, 12.00),
('P002', '2024-02-16', 'South', 'Clothing', 150, 49.99, 8.00),
('P003', '2024-02-17', 'East', 'Electronics', 85, 199.99, 10.00),
('P004', '2024-02-18', 'West', 'Furniture', 40, 599.99, 25.00),
('P005', '2024-02-19', 'North', 'Clothing', 220, 29.99, 5.00),
('P001', '2024-03-15', 'South', 'Electronics', 55, 299.99, 8.00),
('P002', '2024-03-16', 'East', 'Clothing', 130, 49.99, 10.00),
('P003', '2024-03-17', 'West', 'Electronics', 70, 199.99, 12.00),
('P004', '2024-03-18', 'North', 'Furniture', 35, 599.99, 15.00),
('P005', '2024-03-19', 'South', 'Clothing', 180, 29.99, 3.00);
