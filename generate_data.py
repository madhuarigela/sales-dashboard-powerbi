"""
Sales Dashboard - Data Generator
Generates realistic retail sales data for Power BI analysis.
Author: Madhu Arigela
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# --- Config ---
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2024, 12, 31)
N_ORDERS   = 5000

CATEGORIES = {
    "Electronics":   {"products": ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"],
                      "price_range": (5000, 80000)},
    "Clothing":      {"products": ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes"],
                      "price_range": (299, 5000)},
    "Home & Kitchen":{"products": ["Mixer", "Pressure Cooker", "Air Fryer", "Iron", "Fan"],
                      "price_range": (500, 15000)},
    "Books":         {"products": ["Fiction Novel", "Self-Help", "Textbook", "Biography", "Comics"],
                      "price_range": (150, 1500)},
    "Sports":        {"products": ["Cricket Bat", "Football", "Yoga Mat", "Dumbbells", "Cycle"],
                      "price_range": (200, 25000)},
}

CITIES = {
    "Hyderabad": "Telangana", "Mumbai": "Maharashtra", "Bengaluru": "Karnataka",
    "Chennai": "Tamil Nadu", "Delhi": "Delhi", "Pune": "Maharashtra",
    "Kolkata": "West Bengal", "Ahmedabad": "Gujarat", "Jaipur": "Rajasthan",
    "Visakhapatnam": "Andhra Pradesh",
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
CHANNELS = ["Online", "Mobile App", "In-Store"]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

rows = []
for i in range(N_ORDERS):
    category = random.choice(list(CATEGORIES.keys()))
    product  = random.choice(CATEGORIES[category]["products"])
    lo, hi   = CATEGORIES[category]["price_range"]
    price    = round(random.uniform(lo, hi), 2)
    qty      = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
    discount = random.choices([0, 5, 10, 15, 20], weights=[40, 20, 20, 12, 8])[0]
    revenue  = round(price * qty * (1 - discount / 100), 2)
    city     = random.choice(list(CITIES.keys()))
    state    = CITIES[city]
    order_dt = random_date(START_DATE, END_DATE)
    returned = random.choices([0, 1], weights=[92, 8])[0]

    rows.append({
        "order_id":       f"ORD{100000 + i}",
        "order_date":     order_dt.strftime("%Y-%m-%d"),
        "order_time":     order_dt.strftime("%H:%M:%S"),
        "month":          order_dt.strftime("%B"),
        "quarter":        f"Q{(order_dt.month - 1) // 3 + 1}",
        "year":           order_dt.year,
        "category":       category,
        "product":        product,
        "unit_price":     price,
        "quantity":       qty,
        "discount_pct":   discount,
        "revenue":        revenue,
        "city":           city,
        "state":          state,
        "payment_method": random.choice(PAYMENT_METHODS),
        "channel":        random.choice(CHANNELS),
        "returned":       returned,
        "customer_id":    f"CUST{random.randint(1000, 3000):04d}",
    })

df = pd.DataFrame(rows)
df = df.sort_values("order_date").reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/sales_data.csv", index=False)

print(f"Generated {len(df)} orders")
print(f"Total revenue: ₹{df['revenue'].sum():,.0f}")
print(f"Date range: {df['order_date'].min()} → {df['order_date'].max()}")
print(f"\nRevenue by category:")
print(df.groupby("category")["revenue"].sum().sort_values(ascending=False).apply(lambda x: f"₹{x:,.0f}"))
print(f"\nTop 5 cities by revenue:")
print(df.groupby("city")["revenue"].sum().sort_values(ascending=False).head().apply(lambda x: f"₹{x:,.0f}"))
print("\nSaved to data/sales_data.csv")
