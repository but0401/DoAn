import tkinter as tk
from tkinter import ttk, Frame
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import numpy as np

def create_visualizations(df, container):
    """Create and display visualizations in the provided container"""
    # Clear the container
    for widget in container.winfo_children():
        widget.destroy()
    
    # Set modern style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("tab10")
    
    # Create tabs for different visualizations
    tab_control = ttk.Notebook(container)
    
    # Tab 1: Product Analysis
    product_tab = ttk.Frame(tab_control)
    tab_control.add(product_tab, text='Product Analysis')
    
    # Tab 2: Customer Analysis
    customer_tab = ttk.Frame(tab_control)
    tab_control.add(customer_tab, text='Customer Analysis')
    
    # Tab 3: Sales Trends
    trends_tab = ttk.Frame(tab_control)
    tab_control.add(trends_tab, text='Sales Trends')
    
    # Pack the tab control
    tab_control.pack(expand=1, fill="both")
    
    # ============= PRODUCT ANALYSIS TAB =============
    fig1 = plt.figure(figsize=(12, 9), constrained_layout=True)
    
    # 1. Top products by quantity
    ax1 = fig1.add_subplot(2, 1, 1)
    
    # Get top products and show product descriptions if available
    top_products = df.groupby('StockCode')['Quantity'].sum().nlargest(10)
    
    # Try to get descriptions for better labels
    if 'Description' in df.columns:
        labels = []
        for code in top_products.index:
            desc_rows = df[df['StockCode'] == code]['Description'].unique()
            if len(desc_rows) > 0:
                # Truncate long descriptions
                desc = str(desc_rows[0])
                if len(desc) > 20:
                    desc = desc[:18] + '...'
                labels.append(f"{code}\n{desc}")
            else:
                labels.append(code)
    else:
        labels = top_products.index
    
    # Create bar chart with better styling
    bars = ax1.bar(range(len(top_products)), top_products.values, 
            color=sns.color_palette("Blues_d", len(top_products)))
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold')
    
    # Styling
    ax1.set_title('Top 10 Products by Quantity Sold', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Product', fontsize=12)
    ax1.set_ylabel('Total Quantity', fontsize=12)
    ax1.set_xticks(range(len(top_products)))
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 2. Revenue by product (if UnitPrice available)
    ax2 = fig1.add_subplot(2, 1, 2)
    
    if 'UnitPrice' in df.columns:
        # Calculate revenue
        df['Revenue'] = df['Quantity'] * df['UnitPrice']
        top_revenue = df.groupby('StockCode')['Revenue'].sum().nlargest(10)
        
        # Create horizontal bar chart for better readability
        bars = ax2.barh(range(len(top_revenue)), top_revenue.values, 
                color=sns.color_palette("Greens_d", len(top_revenue)))
        
        # Try to get descriptions for better labels
        if 'Description' in df.columns:
            rev_labels = []
            for code in top_revenue.index:
                desc_rows = df[df['StockCode'] == code]['Description'].unique()
                if len(desc_rows) > 0:
                    # Truncate long descriptions
                    desc = str(desc_rows[0])
                    if len(desc) > 20:
                        desc = desc[:18] + '...'
                    rev_labels.append(f"{code}: {desc}")
                else:
                    rev_labels.append(code)
        else:
            rev_labels = top_revenue.index
            
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    f'${width:,.2f}',
                    ha='left', va='center', fontweight='bold')
        
        # Styling
        ax2.set_title('Top 10 Products by Revenue', fontsize=14, fontweight='bold', pad=20)
        ax2.set_xlabel('Revenue ($)', fontsize=12)
        ax2.set_ylabel('Product', fontsize=12)
        ax2.set_yticks(range(len(top_revenue)))
        ax2.set_yticklabels(rev_labels)
        ax2.grid(axis='x', linestyle='--', alpha=0.7)
    else:
        ax2.set_title('Revenue data not available', fontsize=14)
    
    # Add the figure to the product tab
    canvas1 = FigureCanvasTkAgg(fig1, master=product_tab)
    canvas1.draw()
    toolbar1 = NavigationToolbar2Tk(canvas1, product_tab, pack_toolbar=False)
    toolbar1.update()
    
    toolbar1.pack(side=tk.BOTTOM, fill=tk.X)
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # ============= CUSTOMER ANALYSIS TAB =============
    fig2 = plt.figure(figsize=(12, 9), constrained_layout=True)
    
    # 1. Purchases per customer distribution
    ax3 = fig2.add_subplot(2, 1, 1)
    purchases_per_customer = df.groupby('CustomerID')['InvoiceNo'].nunique()
    
    # Create better histogram with KDE
    sns.histplot(purchases_per_customer, bins=30, kde=True, ax=ax3, 
                color='royalblue', edgecolor='black', alpha=0.7)
    
    # Calculate statistics for annotation
    mean_purchases = purchases_per_customer.mean()
    median_purchases = purchases_per_customer.median()
    
    # Add annotations for mean and median
    ax3.axvline(mean_purchases, color='red', linestyle='--', linewidth=2)
    ax3.axvline(median_purchases, color='green', linestyle='--', linewidth=2)
    
    # Add legend
    ax3.text(0.95, 0.95, f"Mean: {mean_purchases:.1f}\nMedian: {median_purchases:.1f}",
            transform=ax3.transAxes, ha='right', va='top',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8))
    
    # Styling
    ax3.set_title('Distribution of Purchases per Customer', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('Number of Purchases', fontsize=12)
    ax3.set_ylabel('Number of Customers', fontsize=12)
    ax3.grid(linestyle='--', alpha=0.7)
    
    # 2. Orders by country (if country column exists)
    ax4 = fig2.add_subplot(2, 1, 2)
    
    if 'Country' in df.columns:
        country_orders = df.groupby('Country')['InvoiceNo'].nunique().nlargest(10)
        
        # Use horizontal bar chart for better label readability
        bars = ax4.barh(range(len(country_orders)), country_orders.values, 
                color=sns.color_palette("plasma", len(country_orders)))
        
        # Add value annotations
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax4.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{int(width):,}',
                    ha='left', va='center', fontweight='bold')
        
        # Styling
        ax4.set_title('Top 10 Countries by Orders', fontsize=14, fontweight='bold', pad=20)
        ax4.set_xlabel('Number of Orders', fontsize=12)
        ax4.set_ylabel('Country', fontsize=12)
        ax4.set_yticks(range(len(country_orders)))
        ax4.set_yticklabels(country_orders.index)
        ax4.grid(axis='x', linestyle='--', alpha=0.7)
    else:
        ax4.set_title('Country data not available', fontsize=14)
    
    # Add the figure to the customer tab
    canvas2 = FigureCanvasTkAgg(fig2, master=customer_tab)
    canvas2.draw()
    toolbar2 = NavigationToolbar2Tk(canvas2, customer_tab, pack_toolbar=False)
    toolbar2.update()
    
    toolbar2.pack(side=tk.BOTTOM, fill=tk.X)
    canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # ============= SALES TRENDS TAB =============
    fig3 = plt.figure(figsize=(12, 9), constrained_layout=True)
    
    # 1. Orders over time
    ax5 = fig3.add_subplot(2, 1, 1)
    
    # Group by date and format properly
    orders_by_date = df.groupby(df['InvoiceDate'].dt.date)['InvoiceNo'].nunique()
    
    # Plot with better styling
    ax5.plot(orders_by_date.index, orders_by_date.values, 
            marker='o', linestyle='-', linewidth=2, markersize=5, 
            color='#1976d2', markerfacecolor='white', markeredgewidth=2)
    
    # Fill area under the curve for better visibility
    ax5.fill_between(orders_by_date.index, orders_by_date.values, 
                    alpha=0.2, color='#1976d2')
    
    # Format date axis
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax5.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
    
    # Styling
    ax5.set_title('Orders Over Time', fontsize=14, fontweight='bold', pad=20)
    ax5.set_xlabel('Date', fontsize=12)
    ax5.set_ylabel('Number of Orders', fontsize=12)
    fig3.autofmt_xdate()  # Rotate date labels automatically
    ax5.grid(linestyle='--', alpha=0.7)
    
    # 2. Sales heatmap by weekday and hour (if time information available)
    ax6 = fig3.add_subplot(2, 1, 2)
    
    try:
        # Extract weekday and hour if possible
        df['Weekday'] = df['InvoiceDate'].dt.day_name()
        df['Hour'] = df['InvoiceDate'].dt.hour
        
        # Create pivot table for heatmap
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hour_pivot = pd.pivot_table(df, 
                                   values='InvoiceNo', 
                                   index='Weekday',
                                   columns='Hour', 
                                   aggfunc='count')
        
        # Reorder weekdays
        if not hour_pivot.empty:
            hour_pivot = hour_pivot.reindex(
                [day for day in weekday_order if day in hour_pivot.index]
            )
            
            # Create heatmap
            sns.heatmap(hour_pivot, cmap="YlGnBu", ax=ax6, cbar_kws={'label': 'Number of Orders'})
            
            # Styling
            ax6.set_title('Orders by Weekday and Hour', fontsize=14, fontweight='bold', pad=20)
            ax6.set_xlabel('Hour of Day', fontsize=12)
            ax6.set_ylabel('Day of Week', fontsize=12)
        else:
            ax6.set_title('Insufficient time data for heatmap', fontsize=14)
    except:
        # Alternative: Revenue trend if time data is insufficient
        if 'UnitPrice' in df.columns:
            df['Revenue'] = df['Quantity'] * df['UnitPrice']
            revenue_by_date = df.groupby(df['InvoiceDate'].dt.date)['Revenue'].sum()
            
            # Plot revenue trend
            ax6.plot(revenue_by_date.index, revenue_by_date.values, 
                    marker='s', linestyle='-', linewidth=2, markersize=5, 
                    color='#2e7d32', markerfacecolor='white', markeredgewidth=2)
            
            # Fill area under the curve
            ax6.fill_between(revenue_by_date.index, revenue_by_date.values, 
                           alpha=0.2, color='#2e7d32')
            
            # Format axes
            ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax6.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
            
            # Add thousand separator to y-axis
            ax6.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'${x:,.0f}'))
            
            # Styling
            ax6.set_title('Revenue Over Time', fontsize=14, fontweight='bold', pad=20)
            ax6.set_xlabel('Date', fontsize=12)
            ax6.set_ylabel('Revenue ($)', fontsize=12)
            ax6.grid(linestyle='--', alpha=0.7)
        else:
            ax6.set_title('Time analysis data not available', fontsize=14)
    
    # Add the figure to the trends tab
    canvas3 = FigureCanvasTkAgg(fig3, master=trends_tab)
    canvas3.draw()
    toolbar3 = NavigationToolbar2Tk(canvas3, trends_tab, pack_toolbar=False)
    toolbar3.update()
    
    toolbar3.pack(side=tk.BOTTOM, fill=tk.X)
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)