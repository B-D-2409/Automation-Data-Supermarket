import pandas as pd
import numpy as np
import os

INPUT_FILE = 'supermarket_sales.csv'
OUTPUT_FILE = 'dirty_sales_data.csv'

def create_dirty_data():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: The file '{INPUT_FILE}' is missing!")
        print("Please download 'supermarket_sales.csv' from Kaggle and place it in this folder.")
        return

    print(f"--- Starting data corruption process on {INPUT_FILE} ---")
    df = pd.read_csv(INPUT_FILE)
    
    duplicates = df.sample(n=50)
    df = pd.concat([df, duplicates], ignore_index=True)
    print("-> Added 50 duplicate rows.")

    random_indices = np.random.choice(df.index, size=30, replace=False)
    df.loc[random_indices, 'Unit price'] = np.nan
    print("-> Injected missing values (NaN) into 'Unit price'.")

    bad_indices = np.random.choice(df.index, size=10, replace=False)
    df.loc[bad_indices, 'Total'] = df.loc[bad_indices, 'Total'] * -1
    print("-> Injected 10 negative values (data errors).")

    df.at[0, 'Total'] = 50000.00
    df.at[0, 'Date'] = '1/15/2019'
    print("-> Injected artificial anomaly ($50,000) on Jan 15th.")

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSUCCESS! File '{OUTPUT_FILE}' has been created.")
    print("You can now run 'python main.py'")

if __name__ == "__main__":
    create_dirty_data()