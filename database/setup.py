
import pandas as pd
import sqlite3
import os

db_path = os.path.join("database", "ecommerce.db")
conn = sqlite3.connect(db_path)

files = {
    "ad_sales": "Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv",
    "total_sales": "Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv",
    "eligibility": "Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv"
}

for table, csv_file in files.items():
    df = pd.read_csv(os.path.join("database", csv_file))
    df.to_sql(table, conn, if_exists="replace", index=False)

print("Database created successfully at", db_path)
conn.close()
