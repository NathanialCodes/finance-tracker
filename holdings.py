import pandas as pd

def load_holdings():
    df = pd.read_excel("tracker.xlsx", sheet_name="Holdings")
    return df