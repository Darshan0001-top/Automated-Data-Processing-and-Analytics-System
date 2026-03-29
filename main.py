import os
import sys
import glob

# Ensure dependencies are available before importing
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please run: pip install pandas numpy matplotlib seaborn")
    sys.exit(1)

from utils.processing import load_data, clean_data, process_data
from utils.analysis import (
    generate_summary_statistics,
    analyze_category_performance,
    identify_top_products,
    generate_report,
    create_visualizations
)

def format_title(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50 + "\n")

def run_pipeline(file_path):
    """
    Run the end-to-end data processing and analytics pipeline.
    """
    format_title(f"Processing Data File: {os.path.basename(file_path)}")
    
    # 1. Data Loading
    df = load_data(file_path)
    if df is None:
        return
        
    # 2. Data Cleaning
    cleaned_df = clean_data(df)
    
    # 3. Data Processing
    processed_df = process_data(cleaned_df)
    
    # 4. Data Analysis & Insights
    format_title("Data Analysis & Insights")
    generate_summary_statistics(processed_df)
    analyze_category_performance(processed_df)
    identify_top_products(processed_df)
    
    # 5. Report Generation & Visualizations
    format_title("Report & Visualizations Generation")
    generate_report(processed_df)
    create_visualizations(processed_df)
    
    print("==================================================")
    print("✅ Pipeline execution completed successfully!")
    print("==================================================\n")

def run_automation(data_dir="data"):
    """
    Wait and scan for all CSV files in the data directory and process them automatically.
    """
    format_title("Automated Batch Processing")
    print(f"Scanning for CSV files in '{data_dir}/'...")
    search_pattern = os.path.join(data_dir, "*.csv")
    csv_files = glob.glob(search_pattern)
    
    if not csv_files:
        print("❌ No CSV files found. Please ensure your files are inside the 'data' directory.\n")
        return
        
    print(f"📄 Found {len(csv_files)} file(s) for processing.")
    for file_path in csv_files:
        run_pipeline(file_path)

def display_menu():
    """
    CLI-Based Interactive Menu System.
    """
    while True:
        print("\n" + "=" * 50)
        print("🚀 Automated Data Processing & Analytics System".center(50))
        print("=" * 50)
        print("[1] Process a specific data file")
        print("[2] Run automated batch processing (all files in data/)")
        print("[3] Exit")
        print("-" * 50)
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
        except EOFError:
            break
            
        if choice == '1':
            filepath = input("Enter the path to the CSV file (e.g., data/sales.csv): ").strip()
            if os.path.exists(filepath):
                run_pipeline(filepath)
            else:
                print("❌ File not found! Please verify the path.\n")
        elif choice == '2':
            run_automation()
        elif choice == '3':
            print("\nExiting the system. Have a productive day! 👋")
            break
        else:
            print("❌ Invalid input! Please select a valid option from the menu.\n")

if __name__ == "__main__":
    # Ensure necessary output directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("utils", exist_ok=True)
    
    # Optional arguments to skip CLI for testing purposes
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_automation()
    else:
        # Run CLI menu
        display_menu()
