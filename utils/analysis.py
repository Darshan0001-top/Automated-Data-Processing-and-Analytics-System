import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_summary_statistics(df):
    """
    Calculate and display key metrics like total revenue, average order value, etc.
    """
    print("--- 📊 Summary Statistics ---")
    total_revenue = df['Total_Sales'].sum()
    avg_order_value = df['Total_Sales'].mean()
    total_items_sold = df['Quantity'].sum()
    
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Average Order Value: ${avg_order_value:,.2f}")
    print(f"Total Items Sold: {total_items_sold}\n")
    
    return {
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value,
        'total_items_sold': total_items_sold
    }

def analyze_category_performance(df):
    """
    Analyze and display category-wise performance.
    """
    print("--- 📂 Category Performance (Revenue & Volume) ---")
    category_group = df.groupby('Category').agg({
        'Total_Sales': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values(by='Total_Sales', ascending=False)
    
    print(category_group.to_string(index=False))
    print("\n")
    return category_group

def identify_top_products(df, top_n=3):
    """
    Identify top-performing products by revenue.
    """
    print(f"--- 🏆 Top {top_n} Products by Revenue ---")
    product_group = df.groupby('Product_Name').agg({
        'Total_Sales': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values(by='Total_Sales', ascending=False).head(top_n)
    
    print(product_group.to_string(index=False))
    print("\n")
    return product_group

def generate_report(df, report_dir="reports"):
    """
    Generate a structured report including summary statistics and category performance,
    saved to a CSV file.
    """
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    report_path = os.path.join(report_dir, "category_summary_report.csv")
    
    # Generate structured CSV report based on category performance
    category_group = df.groupby('Category').agg({
        'Total_Sales': 'sum',
        'Quantity': 'sum'
    }).reset_index().rename(columns={'Total_Sales': 'Total_Revenue', 'Quantity': 'Total_Items_Sold'})
    
    # Adding an average price per category
    category_group['Avg_Item_Revenue'] = category_group['Total_Revenue'] / category_group['Total_Items_Sold']
    category_group['Avg_Item_Revenue'] = category_group['Avg_Item_Revenue'].round(2)
    
    category_group = category_group.sort_values(by='Total_Revenue', ascending=False)
    
    category_group.to_csv(report_path, index=False)
    print(f"✅ Report successfully saved to: {report_path}\n")

def create_visualizations(df, report_dir="reports"):
    """
    Create and save visualizations for the dashboard.
    """
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    try:
        # Configuration for seaborn
        sns.set_theme(style="whitegrid")
        
        # 1. Sales Trends Graph (Line Chart)
        plt.figure(figsize=(10, 6))
        daily_sales = df.groupby('Date')['Total_Sales'].sum().reset_index()
        sns.lineplot(data=daily_sales, x='Date', y='Total_Sales', marker='o', color='b', linewidth=2)
        plt.title('Daily Sales Trend', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Total Revenue ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(report_dir, 'sales_trend.png'), dpi=300)
        plt.close()
        
        # 2. Category Distribution Chart (Bar Chart)
        plt.figure(figsize=(10, 6))
        category_sales = df.groupby('Category')['Total_Sales'].sum().reset_index().sort_values(by='Total_Sales', ascending=False)
        sns.barplot(data=category_sales, x='Category', y='Total_Sales', palette='viridis', hue='Category', legend=False)
        plt.title('Revenue by Category', fontsize=16)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Total Revenue ($)', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(report_dir, 'category_distribution.png'), dpi=300)
        plt.close()
        
        print(f"📈 Visualizations generated and saved in '{report_dir}' directory.\n")
    except Exception as e:
        print(f"Failed to create visualizations: {str(e)}")
        print("Ensure matplotlib and seaborn are installed (pip install matplotlib seaborn).")
