import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import pandas as pd
from datetime import datetime

from data_processing import load_and_process_data
from spade_algorithm import SPADEAlgorithm
from visualization import create_visualizations
from recommendation import generate_recommendations_from_sequences

class SPADEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SPADE Sequential Pattern Mining")
        self.geometry("1200x800")
        
        self.data = None
        self.cleaned_data = None
        self.spade = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create main frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left panel for input and parameters
        left_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # File input section
        file_frame = ttk.Frame(left_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="CSV File:").pack(anchor=tk.W, pady=(0, 5))
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill=tk.X)
        
        self.file_path = tk.StringVar()
        ttk.Entry(file_select_frame, textvariable=self.file_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(file_select_frame, text="Browse...", command=self.browse_file).pack(side=tk.RIGHT)
        
        # Parameters section
        param_frame = ttk.LabelFrame(left_frame, text="Parameters", padding="10")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(param_frame, text="Minimum Support:").pack(anchor=tk.W, pady=(0, 5))
        
        self.min_support = tk.DoubleVar(value=0.01)
        ttk.Entry(param_frame, textvariable=self.min_support).pack(fill=tk.X)
        
        # Buttons section
        button_frame = ttk.LabelFrame(left_frame, text="Actions", padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Load Data", command=self.load_data).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Clean Data", command=self.clean_data).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Run SPADE", command=self.run_spade).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="Generate Statistics", command=self.generate_statistics).pack(fill=tk.X)
        
        # Create notebook for different tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Data tab
        self.data_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.data_tab, text="Data")
        
        # Results tab
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Frequent Patterns")
        
        # Statistics tab
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistics")
        
        # Visualization tab
        self.viz_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_tab, text="Visualizations")
        
        # Recommendations tab
        self.rec_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rec_tab, text="Recommendations")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            self.status_var.set(f"Selected file: {filename}")
    
    def load_data(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        try:
            self.status_var.set("Loading data...")
            self.update_idletasks()
            
            # Load data
            self.data = pd.read_csv(file_path)
            
            # Display data in the data tab
            self.display_data(self.data)
            
            self.status_var.set(f"Loaded {len(self.data)} rows successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.status_var.set("Error loading data.")
    
    def display_data(self, df, tab=None):
        if tab is None:
            tab = self.data_tab
        
        # Clear tab
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Create frame for data table
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for displaying data
        columns = list(df.columns)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack scrollbars and treeview
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns and headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Insert data (first 1000 rows for performance)
        for i, row in df.head(1000).iterrows():
            values = [str(row[col]) for col in columns]
            tree.insert("", tk.END, values=values)
        
        # Show info about displayed rows
        if len(df) > 1000:
            ttk.Label(tab, text=f"Showing first 1000 of {len(df)} rows").pack(pady=5)
    
    def clean_data(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        
        try:
            self.status_var.set("Cleaning data...")
            self.update_idletasks()
            
            # Make a copy of the data
            df = self.data.copy()
            
            # 1. Handle missing values
            df = df.dropna(subset=['CustomerID', 'StockCode', 'InvoiceNo'])
            
            # 2. Convert data types
            df['CustomerID'] = df['CustomerID'].astype(int)
            
            # 3. Convert InvoiceDate to datetime
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            
            # 4. Remove cancelled invoices (those starting with 'C')
            df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
            
            # 5. Remove rows with negative or zero quantities
            df = df[df['Quantity'] > 0]
            
            # 6. Remove rows with negative or zero prices
            df = df[df['UnitPrice'] > 0]
            
            # Store cleaned data
            self.cleaned_data = df
            
            # Display cleaned data
            self.display_data(self.cleaned_data)
            
            # Show before/after statistics
            before_count = len(self.data)
            after_count = len(self.cleaned_data)
            removed = before_count - after_count
            
            messagebox.showinfo(
                "Data Cleaning Results",
                f"Original rows: {before_count}\n"
                f"Cleaned rows: {after_count}\n"
                f"Removed rows: {removed} ({removed/before_count*100:.1f}%)"
            )
            
            self.status_var.set(f"Data cleaned: {after_count} rows remain.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cleaning data: {str(e)}")
            self.status_var.set("Error during data cleaning.")
    
    def run_spade(self):
        if self.cleaned_data is None:
            messagebox.showerror("Error", "Please clean the data first.")
            return
        
        try:
            self.status_var.set("Running SPADE algorithm...")
            self.update_idletasks()
            
            # Get minimum support parameter
            min_support = self.min_support.get()
            if min_support <= 0 or min_support > 1:
                messagebox.showerror("Error", "Minimum support must be between 0 and 1.")
                return
            
            # Initialize SPADE algorithm
            self.spade = SPADEAlgorithm(min_support=min_support)
            
            # Preprocess data
            self.spade.preprocess_data(self.cleaned_data)
            
            # Find frequent sequences
            frequent_sequences = self.spade.find_frequent_sequences()
            
            # Display results
            self.display_frequent_sequences(frequent_sequences)
            
            # Generate recommendations
            self.generate_recommendations()
            
            self.status_var.set(f"Found {len(frequent_sequences)} frequent sequences.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error running SPADE: {str(e)}")
            self.status_var.set("Error running SPADE algorithm.")
    
    def display_frequent_sequences(self, sequences):
        # Clear results tab
        for widget in self.results_tab.winfo_children():
            widget.destroy()
        
        # Create frame
        frame = ttk.Frame(self.results_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=["Sequence", "Support", "Items"], show="headings")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack scrollbars and treeview
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        tree.heading("Sequence", text="Sequence")
        tree.column("Sequence", width=100)
        tree.heading("Support", text="Support")
        tree.column("Support", width=100)
        tree.heading("Items", text="Items")
        tree.column("Items", width=400)
        
        # Insert data
        for i, (sequence, support) in enumerate(sequences):
            # Lookup product descriptions if available
            if 'Description' in self.cleaned_data.columns:
                items_desc = []
                for item in sequence:
                    desc = self.cleaned_data[self.cleaned_data['StockCode'] == item]['Description'].iloc[0] \
                        if len(self.cleaned_data[self.cleaned_data['StockCode'] == item]) > 0 else "Unknown"
                    items_desc.append(f"{item}: {desc}")
                items_str = " -> ".join(items_desc)
            else:
                items_str = " -> ".join(sequence)
            
            tree.insert("", tk.END, values=[str(sequence), f"{support:.4f}", items_str])
    
    def generate_statistics(self):
        if self.cleaned_data is None:
            messagebox.showerror("Error", "Please clean the data first.")
            return
        
        try:
            self.status_var.set("Generating statistics and visualizations...")
            self.update_idletasks()
            
            # Generate stats
            self.display_statistics()
            
            # Generate visualizations
            create_visualizations(self.cleaned_data, self.viz_tab)
            
            self.status_var.set("Statistics and visualizations generated.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating statistics: {str(e)}")
            self.status_var.set("Error generating statistics.")
    
    def display_statistics(self):
        # Clear stats tab
        for widget in self.stats_tab.winfo_children():
            widget.destroy()
        
        # Create scrollable text widget
        text = scrolledtext.ScrolledText(self.stats_tab, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert statistics
        text.insert(tk.END, "=== DATASET STATISTICS ===\n\n")
        
        # Basic dataset stats
        text.insert(tk.END, "OVERVIEW\n")
        text.insert(tk.END, f"Total Transactions: {self.cleaned_data['InvoiceNo'].nunique()}\n")
        text.insert(tk.END, f"Total Products: {self.cleaned_data['StockCode'].nunique()}\n")
        text.insert(tk.END, f"Total Customers: {self.cleaned_data['CustomerID'].nunique()}\n")
        text.insert(tk.END, f"Date Range: {self.cleaned_data['InvoiceDate'].min().date()} to {self.cleaned_data['InvoiceDate'].max().date()}\n\n")
        
        # Product statistics
        text.insert(tk.END, "PRODUCT STATISTICS\n")
        
        product_counts = self.cleaned_data.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False)
        text.insert(tk.END, f"Average quantity per product: {product_counts.mean():.2f}\n")
        text.insert(tk.END, f"Median quantity per product: {product_counts.median():.2f}\n")
        
        text.insert(tk.END, "\nTop 10 Products by Quantity:\n")
        for i, (product, count) in enumerate(product_counts.head(10).items(), 1):
            desc = self.cleaned_data[self.cleaned_data['StockCode'] == product]['Description'].iloc[0] \
                if 'Description' in self.cleaned_data.columns and len(self.cleaned_data[self.cleaned_data['StockCode'] == product]) > 0 else "Unknown"
            text.insert(tk.END, f"{i}. {product} ({desc}): {count} units\n")
        
        # Customer statistics
        text.insert(tk.END, "\nCUSTOMER STATISTICS\n")
        
        customer_orders = self.cleaned_data.groupby('CustomerID')['InvoiceNo'].nunique()
        text.insert(tk.END, f"Average invoices per customer: {customer_orders.mean():.2f}\n")
        text.insert(tk.END, f"Median invoices per customer: {customer_orders.median():.2f}\n")
        text.insert(tk.END, f"Maximum invoices by a customer: {customer_orders.max()}\n\n")
        
        # Country statistics
        text.insert(tk.END, "COUNTRY STATISTICS\n")
        
        if 'Country' in self.cleaned_data.columns:
            country_orders = self.cleaned_data.groupby('Country')['InvoiceNo'].nunique().sort_values(ascending=False)
            text.insert(tk.END, "Top 10 Countries by Number of Orders:\n")
            for i, (country, count) in enumerate(country_orders.head(10).items(), 1):
                text.insert(tk.END, f"{i}. {country}: {count} orders\n")
        
        text.configure(state='disabled')  # Make read-only
    
    def generate_recommendations(self):
        if not hasattr(self, 'spade') or self.spade is None:
            return
        
        # Clear recommendations tab
        for widget in self.rec_tab.winfo_children():
            widget.destroy()
        
        # Create controls frame
        controls_frame = ttk.Frame(self.rec_tab)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Product selection dropdown
        ttk.Label(controls_frame, text="Select a product:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Get unique products
        products = sorted(self.cleaned_data['StockCode'].unique())
        
        # Create combobox
        self.selected_product = tk.StringVar()
        product_combo = ttk.Combobox(controls_frame, textvariable=self.selected_product, values=products, width=30)
        product_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Find button
        ttk.Button(controls_frame, text="Find Recommendations", 
                   command=self.show_product_recommendations).pack(side=tk.LEFT)
        
        # Results frame
        self.rec_results_frame = ttk.LabelFrame(self.rec_tab, text="Product Recommendations")
        self.rec_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Initial message
        ttk.Label(self.rec_results_frame, 
                 text="Select a product and click 'Find Recommendations' to see products frequently purchased together.").pack(pady=20)
    
    def show_product_recommendations(self):
        product = self.selected_product.get()
        if not product:
            messagebox.showinfo("Info", "Please select a product first.")
            return
        
        # Clear previous results
        for widget in self.rec_results_frame.winfo_children():
            widget.destroy()
        
        # Find sequences containing the selected product
        recommendations = {}
        
        for seq, support in self.spade.frequent_sequences:
            if product in seq:
                # Find position of product in sequence
                pos = seq.index(product)
                
                # Get products that appear after the selected product
                for i in range(pos + 1, len(seq)):
                    next_item = seq[i]
                    if next_item != product:  # Don't recommend the same product
                        if next_item in recommendations:
                            recommendations[next_item] = max(recommendations[next_item], support)
                        else:
                            recommendations[next_item] = support
        
        # Sort recommendations by support
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        if not sorted_recs:
            ttk.Label(self.rec_results_frame, 
                      text=f"No recommendations found for product {product}.").pack(pady=20)
            return
        
        # Get product description
        if 'Description' in self.cleaned_data.columns:
            prod_desc = self.cleaned_data[self.cleaned_data['StockCode'] == product]['Description'].iloc[0] \
                if len(self.cleaned_data[self.cleaned_data['StockCode'] == product]) > 0 else "Unknown"
            product_info = f"{product} ({prod_desc})"
        else:
            product_info = product
        
        # Display header
        ttk.Label(self.rec_results_frame, 
                  text=f"Recommendations for {product_info}", 
                  font=("Helvetica", 12, "bold")).pack(pady=(10, 20))
        
        # Create frame for results
        results_frame = ttk.Frame(self.rec_results_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        tree = ttk.Treeview(results_frame, columns=["Product", "Description", "Confidence"], show="headings")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        # Pack scrollbar and treeview
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        tree.heading("Product", text="Product Code")
        tree.column("Product", width=100)
        tree.heading("Description", text="Description")
        tree.column("Description", width=300)
        tree.heading("Confidence", text="Confidence")
        tree.column("Confidence", width=100)
        
        # Insert recommendations
        for product, confidence in sorted_recs[:20]:  # Show top 20 recommendations
            if 'Description' in self.cleaned_data.columns:
                desc = self.cleaned_data[self.cleaned_data['StockCode'] == product]['Description'].iloc[0] \
                    if len(self.cleaned_data[self.cleaned_data['StockCode'] == product]) > 0 else "Unknown"
            else:
                desc = "N/A"
            
            tree.insert("", tk.END, values=[product, desc, f"{confidence:.4f}"])