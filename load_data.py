
#import pandas as pd
#import sqlite3

#conn = sqlite3.connect("ecom_data.db")

#pd.read_csv("database/ad_sales.csv").to_sql("ad_sales", conn, if_exists="replace", index=False)
#pd.read_csv("database/total_sales.csv").to_sql("total_sales", conn, if_exists="replace", index=False)
#pd.read_csv("database/eligibility.csv").to_sql("eligibility", conn, if_exists="replace", index=False)

#conn.close()
#print("✅ Data loaded into ecom_data.db")

import sqlite3
import pandas as pd

# Load CSV files
total_sales = pd.read_csv("database/total_sales.csv")
ad_sales = pd.read_csv("database/ad_sales.csv")
eligibility = pd.read_csv("database/eligibility.csv")

# Connect to SQLite DB
conn = sqlite3.connect("ecom_data.db")

# Save DataFrames as tables
total_sales.to_sql("total_sales", conn, if_exists="replace", index=False)
ad_sales.to_sql("ad_sales", conn, if_exists="replace", index=False)
eligibility.to_sql("eligibility", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("✅ Data loaded into ecom_data.db")

