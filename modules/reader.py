import pandas as pd
from pathlib import Path

def read_data(path):
    """
    Reads CSV, XLSX, or JSON into a pandas DataFrame.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix in [".csv"]:
        df = pd.read_csv(path)
    elif suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    elif suffix in [".json"]:
        df = pd.read_json(path)
    else:
        raise ValueError("Unsupported file type. Use .csv, .xlsx, or .json")

    if df.empty:
        raise ValueError("Loaded dataframe is empty")

    return df
