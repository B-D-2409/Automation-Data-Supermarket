import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_dataset():
    print("Generating synthetic Kaggle dataset...")
    
    rows = 1000
    branches = ['A', 'B', 'C']
    cities = {'A': 'Yangon', 'B': 'Mandalay', 'C': 'Naypyitaw'}
    products = ['Health and beauty', 'Electronic accessories', 'Home and lifestyle', 
                'Sports and travel', 'Food and beverages', 'Fashion accessories']
    payments = ['Ewallet', 'Cash', 'Credit card']
    
    data = []
    
    for _ in range(rows):
        branch = random.choice(branches)
        city = cities[branch]
        price = round(random.uniform(10, 100), 2)
        qty = random.randint(1, 10)
        total_no_tax = price * qty
        tax = round(total_no_tax * 0.05, 4)
        total = round(total_no_tax + tax, 4)
        
        date_obj = datetime(2019, 1, 1) + timedelta(days=random.randint(0, 89))
        
        row = {
            "Invoice ID": f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}",
            "Branch": branch,
            "City": city,
            "Customer type": random.choice(['Member', 'Normal']),
            "Gender": random.choice(['Male', 'Female']),
            "Product line": random.choice(products),
            "Unit price": price,
            "Quantity": qty,
            "Tax 5%": tax,
            "Total": total,
            "Date": date_obj.strftime("%m/%d/%Y"),
            "Time": f"{random.randint(10,20)}:{random.randint(0,59):02d}",
            "Payment": random.choice(payments),
            "cogs": round(total_no_tax, 2),
            "gross margin percentage": 4.7619,
            "gross income": tax,
            "Rating": round(random.uniform(4, 10), 1)
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv("supermarket_sales.csv", index=False)
    print("SUCCESS! File 'supermarket_sales.csv' has been created.")

if __name__ == "__main__":
    create_dataset()