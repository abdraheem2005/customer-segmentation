import pandas as pd
import numpy as np

def load_data(filepath: str) -> pd.DataFrame:
    """Load dataset from CSV or other supported format."""
    return pd.read_csv(filepath)

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values intelligently per column type."""
    # Drop rows where CustomerID is missing - essential for segmentation
    df = df.dropna(subset=['CustomerID'])

    # Fill missing Description with 'Unknown'
    df['Description'] = df['Description'].fillna('Unknown')

    return df

def find_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Find duplicate transactions based on InvoiceNo, StockCode, CustomerID"""
    duplicates = df[df.duplicated(subset=['InvoiceNo', 'StockCode', 'CustomerID'], keep=False)]
    return duplicates

def calculate_rfm(df: pd.DataFrame, current_date: pd.Timestamp) -> pd.DataFrame:
    """Calculate RFM features for each customer."""
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Aggregate data to customer level
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (current_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',                                 # Frequency
        'Quantity': 'sum',                                      # Quantity sum for Monetary calculation
        'UnitPrice': 'mean'                                     # Average price per unit - optional additional feature
    }).rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency'
    })

    # Calculate Monetary value as total spent = sum(Quantity * UnitPrice) per customer
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    monetary = df.groupby('CustomerID')['TotalPrice'].sum()
    rfm['Monetary'] = monetary

    # Some customers might have 0 or negative monetary value; consider filtering
    rfm = rfm[rfm['Monetary'] > 0]

    return rfm.reset_index()

def main():
    # Load Dataset - replace with your actual file path
    filepath = 'retail_dataset.csv'
    df = load_data(filepath)

    # Clean Data: handle Missing Values
    df = handle_missing_values(df)

    # Find Duplicates
    duplicates = find_duplicates(df)
    print(f"Number of duplicate transactions found: {len(duplicates)}")

    # Remove duplicates if needed
    df = df.drop_duplicates(subset=['InvoiceNo', 'StockCode', 'CustomerID'])

    # Calculate RFM Features using a reference current date (e.g., max invoice date + 1 day)
    current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm_features = calculate_rfm(df, current_date)

    print(rfm_features.head())

if __name__ == '__main__':
    main()