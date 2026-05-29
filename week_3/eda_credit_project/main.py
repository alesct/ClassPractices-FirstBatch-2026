import openml
import pandas as pd

def download_data():
    print("Connecting to OpenML to get 'credit-g'...")
    dataset = openml.datasets.get_dataset(31)
    
    X, y, _, _ = dataset.get_data(target='class', dataset_format="dataframe")
    
    df = pd.concat([X, y], axis=1)
    
    df.to_csv("credit_data.csv", index=False)
    print("✅ Success! 'credit_data.csv' created.")

if __name__ == "__main__":
    download_data()