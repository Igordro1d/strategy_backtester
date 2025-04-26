import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        df = pd.read_csv(self.filepath)

        #correct datetime parsing
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Index', inplace=True)
            df.sort_index(inplace=True)
        else:
            raise ValueError("No date column found in data.")

        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing {col} column")

        df = df.ffill.dropna()
        return df