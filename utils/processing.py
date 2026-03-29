import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Read data from CSV files using Python.
    Displays dataset overview.
    """
    try:
        print(f"Loading data from {file_path}...")
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully!")
        print(f"Dataset Overview (First 3 rows):")
        print(df.head(3).to_string())
        print(f"\nDataset Shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_data(df):
    """
    Handle missing values, remove duplicates, and format data properly.
    """
    if df is None:
        return None
        
    print("Initiating Data Cleaning...")
    initial_rows = len(df)
    
    # 1. Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    
    # 2. Handle missing values
    # For missing 'Price', we fill with the median price of the available data
    if df['Price'].isnull().any():
        median_price = df['Price'].median()
        df['Price'] = df['Price'].fillna(median_price)
        print(f"Filled missing 'Price' values with median: ${median_price:.2f}")
    
    # Drop rows where 'Date' is missing since time-series analysis requires dates
    missing_dates = df['Date'].isnull().sum()
    if missing_dates > 0:
        df = df.dropna(subset=['Date'])
        print(f"Dropped {missing_dates} rows with missing 'Date'.")
        
    print(f"Data Cleaning Completed:")
    print(f" - Duplicates removed: {duplicates_removed}")
    print(f" - Current Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")
    
    return df

def process_data(df):
    """
    Calculate total sales, and perform necessary transformations.
    """
    if df is None or df.empty:
        return None
        
    print("Initiating Data Processing...")
    
    # Calculate total sales
    df['Total_Sales'] = df['Price'] * df['Quantity']
    
    # Ensure 'Date' is properly formatted as datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    print("Data processing completed: Added 'Total_Sales' column and formatted Date.\n")
    return df
