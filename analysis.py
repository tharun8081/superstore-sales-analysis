import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="superstore_db"
)

print("Connected successfully!")
query = "SELECT * FROM superstore"

# Step 3: Load into pandas
df = pd.read_sql(query, conn)

# Step 4: Check data
print(df.head())
print(df.info())
# Convert date columns properly
df['order_date_clean'] = pd.to_datetime(df['order_date_clean'])
df['ship_date_clean'] = pd.to_datetime(df['ship_date_clean'])
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['order_id'].nunique()

print("Total Sales:", total_sales)
print("Total Profit:", total_profit)
print("Total Orders:", total_orders)
monthly_sales = df.groupby(['order_year','order_month'])['Sales'].sum().reset_index()

monthly_sales['date'] = monthly_sales['order_year'].astype(str) + "-" + monthly_sales['order_month'].astype(str)

import matplotlib.pyplot as plt

plt.figure()
plt.plot(monthly_sales['date'], monthly_sales['Sales'])
plt.xticks(rotation=90)
plt.title("Monthly Sales Trend")
plt.tight_layout()
plt.savefig("sales_trend.png")
plt.show()
top_products = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)

plt.figure()
top_products.plot(kind='bar')
plt.title("Top 10 Sub-Categories")
plt.tight_layout()
plt.savefig("top_products.png")
plt.show()
category = df.groupby('Category')['Sales'].sum()

plt.figure()
category.plot(kind='pie', autopct='%1.1f%%')
plt.title("Category Contribution")
plt.ylabel("")
plt.savefig("category.png")
plt.show()
region = df.groupby('Region')['Sales'].sum()

plt.figure()
region.plot(kind='bar')
plt.title("Region Performance")
plt.savefig("region.png")
plt.show()
import seaborn as sns

plt.figure()
sns.scatterplot(data=df, x='Sales', y='Profit')
plt.title("Sales vs Profit")
plt.savefig("sales_vs_profit.png")
plt.show()
plt.figure()
sns.boxplot(x='Discount', y='Profit', data=df)
plt.title("Discount vs Profit")
plt.savefig("discount_profit.png")
plt.show()
plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
category.plot(kind='pie', autopct='%1.1f%%')
plt.title("Category")

plt.subplot(2,2,2)
region.plot(kind='bar')
plt.title("Region")

plt.subplot(2,2,3)
top_products.plot(kind='bar')
plt.title("Top Products")

plt.subplot(2,2,4)
plt.plot(monthly_sales['Sales'])
plt.title("Sales Trend")

plt.tight_layout()
plt.savefig("dashboard.png")
plt.show()