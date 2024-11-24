import pandas as pd

def load_data(file):
    if file:
        data = pd.read_csv(file)
        return data
    else:
        raise ValueError("No file provided")
