import sv_ttk
from gui import SPADEApp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Make sure the data directory exists
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(data_dir, exist_ok=True)

if __name__ == "__main__":
    app = SPADEApp()
    app.mainloop()