# 🛒 Retail Sales Dashboard — Power BI

**Data Analyst Portfolio Project | Madhu Arigela**

A production-style Power BI dashboard analyzing 5,000 retail orders across 2 years (2023–2024), 
10 Indian cities, 5 product categories, and 5 payment methods.

---

## 📊 Dashboard pages

| Page | Key visuals |
|------|-------------|
| **Executive Overview** | Total revenue, orders, AOV, return rate KPIs |
| **Sales Trends** | Monthly revenue line chart, QoQ growth, seasonal peaks |
| **Category Analysis** | Revenue by category (bar), product-level drill-down |
| **Geographic View** | City/state revenue map, top 10 city ranking |
| **Payment & Channel** | UPI vs Credit Card split, Online vs In-Store vs App |
| **Returns Analysis** | Return rate by category, city, payment method |

---

## 🔑 Key findings

- **Electronics dominates**: 64% of total revenue (₹7.5 Cr of ₹11.7 Cr total)
- **Visakhapatnam ranks #2** in city revenue despite being a Tier-2 city — opportunity signal
- **UPI adoption**: highest in Online channel; Cash on Delivery still significant for In-Store
- **Q4 peak**: November–December orders spike 28% vs Q1 average (festive season effect)
- **Return rate**: 8% overall; highest in Electronics (12%) — quality/expectation mismatch
- **AOV**: ₹23,352 overall; Sports category has highest average basket size

---

## 🗂️ Repository structure

```
sales-dashboard-powerbi/
├── data/
│   └── sales_data.csv          # 5,000 orders, 19 columns
├── generate_data.py            # Python script to regenerate dataset
├── dashboard/
│   └── Sales_Dashboard.pbix   # Power BI file (build steps below)
├── screenshots/
│   └── [dashboard screenshots]
└── README.md
```

---

## 🚀 How to run

### Step 1: Generate the dataset
```bash
pip install pandas numpy
python generate_data.py
# Output: data/sales_data.csv
```

### Step 2: Load into Power BI Desktop
1. Open Power BI Desktop (free download: powerbi.microsoft.com)
2. **Get Data → Text/CSV** → select `data/sales_data.csv`
3. Power Query auto-detects all 19 columns — click **Load**

### Step 3: Build the data model

In Power Query Editor, add these calculated columns:

```
Revenue Category =
IF([revenue] < 5000, "Low",
IF([revenue] < 20000, "Medium", "High"))
```

```
Month Number =
SWITCH([month],
"January",1, "February",2, "March",3, "April",4,
"May",5, "June",6, "July",7, "August",8,
"September",9, "October",10, "November",11, "December",12)
```

### Step 4: Create DAX measures

```dax
Total Revenue = SUM(sales_data[revenue])

Total Orders = COUNTROWS(sales_data)

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Return Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(sales_data), sales_data[returned] = 1),
    [Total Orders],
    0
) * 100

MoM Revenue Growth % = 
VAR CurrentMonth = [Total Revenue]
VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(sales_data[order_date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0) * 100

Revenue YTD = TOTALYTD([Total Revenue], sales_data[order_date])
```

### Step 5: Build visuals (page by page)

**Page 1 — Executive Overview**
- 4 KPI cards: Total Revenue, Total Orders, AOV, Return Rate %
- Line chart: order_date (month) vs Total Revenue
- Donut: channel split

**Page 2 — Sales Trends**
- Line + column combo: Monthly revenue + order count
- Matrix: Year × Quarter revenue with conditional formatting

**Page 3 — Category Analysis**
- Clustered bar: category vs Total Revenue (sorted desc)
- Table: product-level revenue, orders, AOV

**Page 4 — Geographic View**
- Filled map: state → revenue (requires Bing Maps)
- Bar chart: top 10 cities by revenue

**Page 5 — Payment & Channel**
- Pie: payment_method split
- Stacked bar: channel × payment_method

**Page 6 — Returns**
- Bar: return rate % by category
- Table: city vs return count vs return rate

---

## 📋 Dataset columns

| Column | Type | Description |
|--------|------|-------------|
| order_id | String | Unique order identifier |
| order_date | Date | YYYY-MM-DD |
| order_time | Time | HH:MM:SS |
| month | String | Month name |
| quarter | String | Q1–Q4 |
| year | Integer | 2023 or 2024 |
| category | String | Product category |
| product | String | Product name |
| unit_price | Float | Price before discount (₹) |
| quantity | Integer | Units ordered |
| discount_pct | Integer | Discount % (0/5/10/15/20) |
| revenue | Float | Net revenue after discount (₹) |
| city | String | Indian city |
| state | String | Indian state |
| payment_method | String | UPI / Credit Card / etc |
| channel | String | Online / Mobile App / In-Store |
| returned | Integer | 1 = returned, 0 = kept |
| customer_id | String | Customer identifier |

---

## 🛠️ Tech stack

- **Python** (pandas, numpy) — data generation
- **Power BI Desktop** — dashboard & DAX measures
- **CSV** — portable data format

---

## 👤 Author

**Madhu Arigela** — Data Analyst Portfolio  
[linkedin.com/in/madhuarigela](https://linkedin.com/in/madhuarigela) | [github.com/madhuarigela](https://github.com/madhuarigela)
