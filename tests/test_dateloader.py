import unittest
from unittest.mock import patch
import pandas as pd
from core.dataloader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.good_df = pd.DataFrame({
            'Index': [0, 1],
            'Date': ['2025-01-01', '2025-01-02'],
            'Open': [100, 106],
            'High': [110, 112],
            'Low': [90, 101],
            'Close': [105, 110],
            'Volume': [10000, 15000]
        })
        self.no_date_df = pd.DataFrame({
            'Index': [0],
            'Open': [100],
            'High': [110],
            'Low': [90],
            'Close': [105],
            'Volume': [10000]
        })
        self.no_volume_df = pd.DataFrame({
            'Index': [0],
            'Date': ['2025-01-01'],
            'Open': [100],
            'High': [110],
            'Low': [90],
            'Close': [105]
        })

    @patch('core.dataloader.pd.read_csv')
    def test_load_data_success(self, mock_read_csv):
        mock_read_csv.return_value = self.good_df.copy()

        loader = DataLoader('fake_path.csv')
        df = loader.load_data()

        self.assertFalse(df.empty)
        self.assertIn(0, df.index)
        self.assertIn(1, df.index)

        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.assertIn(col, df.columns)

        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['Date']))

    @patch('core.dataloader.pd.read_csv')
    def test_missing_date_column(self, mock_read_csv):
        mock_read_csv.return_value = self.no_date_df.copy()

        loader = DataLoader('fake_path.csv')
        with self.assertRaises(ValueError) as context:
            loader.load_data()
        self.assertIn("No date column found", str(context.exception))

    @patch('core.dataloader.pd.read_csv')
    def test_missing_required_columns(self, mock_read_csv):
        mock_read_csv.return_value = self.no_volume_df.copy()

        loader = DataLoader('fake_path.csv')
        with self.assertRaises(ValueError) as context:
            loader.load_data()
        self.assertIn("Missing Volume column", str(context.exception))

if __name__ == '__main__':
    unittest.main()
