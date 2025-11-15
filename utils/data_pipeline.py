# utils/data_pipeline.py
import pandas as pd

def load_product_data(csv_path):
    df = pd.read_csv(csv_path)
    # Clean and standardize product descriptions
    df['description'] = df['description'].str.lower().str.strip()
    return df
