import pandas as pd

def get_data_info(file_path):
    df = pd.read_csv(file_path)
    
    specs = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "column_names": list(df.columns)
    }
    
    missing = df.isnull().sum().to_dict()
    
    return specs, missing