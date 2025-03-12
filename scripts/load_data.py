import pandas as pd
import os

def load_data():
    data_folder = os.path.join('..', 'data')
    file_path = os.path.join(data_folder, 'forest_threats_dataset.csv')
    df = pd.read_csv(file_path, parse_dates=['Date'], date_format='%d %B')
    return df

if __name__ == "__main__":
    data = load_data()
    print(data.head())
    print(data.columns)