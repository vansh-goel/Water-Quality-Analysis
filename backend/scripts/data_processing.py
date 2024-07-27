import pandas as pd

def load_data(file):
    """Load data from a CSV file."""
    return pd.read_csv(file)

def to_numeric_safe(s):
    return pd.to_numeric(s, errors='coerce')

def process_data(df):
    parameters = ['Temperature', 'Dissolved Oxygen (mg/L)', 'pH', 'Conductivity (?mhos/cm)',
                  'BOD (mg/L)', 'Nitrate N + Nitrite N(mg/L)', 'Fecal Coliform (MPN/100ml)',
                  'Total Coliform (MPN/100ml)']

    for param in parameters:
        min_col = next((col for col in df.columns if col.startswith(param) and 'Min' in col), None)
        max_col = next((col for col in df.columns if col.startswith(param) and 'Max' in col), None)
        if min_col and max_col:
            df[min_col] = to_numeric_safe(df[min_col])
            df[max_col] = to_numeric_safe(df[max_col])
            df[f"Avg_{param.split()[0]}"] = (df[min_col] + df[max_col]) / 2

    return df

