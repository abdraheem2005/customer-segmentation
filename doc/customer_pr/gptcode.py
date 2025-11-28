import pandas as pd
import numpy as np

# --------------------------------------------------------
# Load and Inspect
# --------------------------------------------------------

def load_data(path):
    """Load retail dataset."""
    df = pd.read_csv(path, encoding='ISO-8859-1')
    return df


# --------------------------------------------------------
# Data Cleaning Functions
# --------------------------------------------------------

def clean_missing_values(df):
    """
    Handle missing values:
    - Drop rows with missing CustomerID
    - Fill missing Description
    - Impute numeric columns where needed
    """
    df = df.copy()

    # Drop rows without CustomerID (cannot perform customer segmentation)
    df = df.dropna(subset=['CustomerID'])

    # Fill missing descriptions
    df['Description'] = df['Description'].fillna("Unknown Description")

    # For other numeric fields (if any)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    return df


def remove_duplicates(df):
    """Remove duplicate rows."""
    df = df.copy()
    df = df.drop_duplicates()
    return df


# --------------------------------------------------------
# RFM Feature Engineering
# --------------------------------------------------------

def calculate_rfm(df):
    """
    Compute Recency, Frequency, Monetary features.
    """
    df = df.copy()

    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Compute monetary value (line item price)
    df['Amount'] = df['Quantity'] * df['UnitPrice']

    # Snapshot date (1 day after last invoice)
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',                                   # Frequency
        'Amount': 'sum'                                           # Monetary
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    return rfm


# --------------------------------------------------------
# Advanced Feature Engineering
# --------------------------------------------------------

def engineer_additional_features(df):
    """Create advanced features beyond RFM."""
    df = df.copy()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Amount'] = df['Quantity'] * df['UnitPrice']

    feature_df = df.groupby('CustomerID').apply(lambda x: pd.Series({
        # Product Diversity
        'UniqueProducts': x['StockCode'].nunique(),
        'VarietyIndex': x['StockCode'].nunique() / x['Quantity'].sum(),

        # Purchasing Patterns
        'AvgBasketSize': x.groupby('InvoiceNo')['Quantity'].sum().mean(),
        'AvgOrderValue': x['Amount'].sum() / x['InvoiceNo'].nunique(),
        'PriceMean': x['UnitPrice'].mean(),
        'PriceStd': x['UnitPrice'].std(),
        'ReturnRate': (x['Quantity'] < 0).sum() / len(x),

        # Temporal Features
        'ActiveDays': (x['InvoiceDate'].max() - x['InvoiceDate'].min()).days,
        'ActiveMonths': x['InvoiceDate'].dt.to_period('M').nunique(),
        'MeanInterpurchaseTime': x['InvoiceDate'].diff().dt.days.mean(),
        'WeekendPurchaseRatio': (x['InvoiceDate'].dt.weekday >= 5).mean(),
        'MorningPurchaseRatio': ((x['InvoiceDate'].dt.hour >= 6) &
                                 (x['InvoiceDate'].dt.hour < 12)).mean(),

        # Geographical Features
        'NumCountries': x['Country'].nunique()
    }))

    return feature_df


# --------------------------------------------------------
# Combine All Features
# --------------------------------------------------------

def build_customer_segmentation_dataset(df):
    """Wrapper pipeline to create cleaned and feature-engineered dataset."""
    df = clean_missing_values(df)
    df = remove_duplicates(df)

    rfm = calculate_rfm(df)
    extra_features = engineer_additional_features(df)

    # Combine
    final_df = rfm.join(extra_features, how='left')

    return final_df


# --------------------------------------------------------
# Example Usage
# --------------------------------------------------------

# df = load_data("OnlineRetail.csv")
# customer_df = build_customer_segmentation_dataset(df)
# print(customer_df.head())
