import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("supermarket_sales.csv")


print(df.head())


plt.figure(figsize=(10, 6))
sns.countplot(x='Payment', data=df)
plt.title("Payment Methods Distribution")
plt.show() 