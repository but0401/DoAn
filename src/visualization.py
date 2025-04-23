import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

def create_visualizations(df, container):
    """Create and display visualizations in the provided container"""
    # Clear the container
    for widget in container.winfo_children():
        widget.destroy()
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(12, 10))
    fig.subplots_adjust(hspace=0.4)
    
    # 1. Product quantity distribution
    ax1 = fig.add_subplot(2, 2, 1)
    top_products = df.groupby('StockCode')['Quantity'].sum().nlargest(10)
    top_products.plot(kind='bar', ax=ax1)
    ax1.set_title('Top 10 Products by Quantity Sold')
    ax1.set_xlabel('Product Code')
    ax1.set_ylabel('Total Quantity')
    plt.xticks(rotation=45)
    
    # 2. Orders by country (if country column exists)
    ax2 = fig.add_subplot(2, 2, 2)
    if 'Country' in df.columns:
        country_orders = df.groupby('Country')['InvoiceNo'].nunique().nlargest(10)
        country_orders.plot(kind='bar', ax=ax2)
        ax2.set_title('Top 10 Countries by Orders')
        ax2.set_xlabel('Country')
        ax2.set_ylabel('Number of Orders')
        plt.xticks(rotation=45)
    else:
        ax2.set_title('Country data not available')
    
    # 3. Orders over time
    ax3 = fig.add_subplot(2, 2, 3)
    orders_by_date = df.groupby(df['InvoiceDate'].dt.date)['InvoiceNo'].nunique()
    orders_by_date.plot(ax=ax3)
    ax3.set_title('Orders Over Time')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Number of Orders')
    
    # 4. Purchases per customer distribution
    ax4 = fig.add_subplot(2, 2, 4)
    purchases_per_customer = df.groupby('CustomerID')['InvoiceNo'].nunique()
    sns.histplot(purchases_per_customer, bins=30, ax=ax4)
    ax4.set_title('Distribution of Purchases per Customer')
    ax4.set_xlabel('Number of Purchases')
    ax4.set_ylabel('Number of Customers')
    
    # Add the figure to the visualization tab
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)