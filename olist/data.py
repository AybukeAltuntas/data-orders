from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.

    Methods:
        get_data():
            Loads and returns a dictionary where keys are dataset names (e.g., 'sellers', 'orders')
            and values are pandas DataFrames loaded from corresponding CSV files.

        ping():
            Prints "pong" to confirm the method is callable.
    """
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # CSV dosyalarının bulunduğu klasör
        base_path = Path("~/.workintech/olist/data/csv").expanduser()
        file_paths = list(base_path.glob('*.csv'))  # tüm csv dosyalarını al

        data = {}
        for path in file_paths:
            name = path.name

            # 'olist_' önekini kaldır
            if name.startswith('olist_'):
                name = name[len('olist_'):]
            # '_dataset.csv' sonekini kaldır
            if name.endswith('_dataset.csv'):
                name = name[:-len('_dataset.csv')]
            # sadece '.csv' sonekini kaldır (kalanlar için)
            elif name.endswith('.csv'):
                name = name[:-len('.csv')]

            # DataFrame'i sözlüğe ekle
            data[name] = pd.read_csv(path)

        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
