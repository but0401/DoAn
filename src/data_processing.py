import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """Load data from CSV file"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found.")
            return pd.DataFrame()
        
        # Load the data
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def clean_data(df):
    """Clean the dataset"""
    if df.empty:
        return df
    
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Handle missing values
    cleaned_df = cleaned_df.dropna(subset=['CustomerID', 'StockCode', 'InvoiceNo'])
    
    # Convert data types
    if 'CustomerID' in cleaned_df.columns:
        cleaned_df['CustomerID'] = pd.to_numeric(cleaned_df['CustomerID'], errors='coerce')
        cleaned_df = cleaned_df.dropna(subset=['CustomerID'])
        cleaned_df['CustomerID'] = cleaned_df['CustomerID'].astype(int)
    
    # Convert InvoiceDate to datetime
    if 'InvoiceDate' in cleaned_df.columns:
        cleaned_df['InvoiceDate'] = pd.to_datetime(cleaned_df['InvoiceDate'], errors='coerce')
        cleaned_df = cleaned_df.dropna(subset=['InvoiceDate'])
    
    # Remove rows with negative or zero quantities
    if 'Quantity' in cleaned_df.columns:
        cleaned_df = cleaned_df[cleaned_df['Quantity'] > 0]
        
    # Remove rows with negative or zero prices
    if 'UnitPrice' in cleaned_df.columns:
        cleaned_df = cleaned_df[cleaned_df['UnitPrice'] > 0]
    
    return cleaned_df

def load_and_process_data(file_path):
    """Load and clean data from CSV file"""
    df = load_data(file_path)
    if not df.empty:
        df = clean_data(df)
    return df