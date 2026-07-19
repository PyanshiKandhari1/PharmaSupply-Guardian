import pandas as pd

# ======================================================
# PharmaSupply Guardian
# Drug Shortage & Expiry Risk Intelligence Platform
# ======================================================

# -------------------------
# LOAD DATASET
# -------------------------

df = pd.read_csv("data/inventory.csv")

print("Dataset Loaded Successfully!")

# -------------------------
# DATE COLUMNS
# -------------------------

date_columns = [
    "Received_Date",
    "Last_Purchase_Date",
    "Expiry_Date",
    "Audit_Date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col])

# -------------------------
# PERCENTAGE COLUMNS
# -------------------------

percent_columns = [
    "Supplier_OnTime_Pct",
    "Audit_Variance_Pct",
    "Demand_Forecast_Accuracy_Pct"
]

for col in percent_columns:
    df[col] = (
        df[col]
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# -------------------------
# CURRENCY COLUMNS
# -------------------------

money_columns = [
    "Unit_Cost_USD",
    "Last_Purchase_Price_USD",
    "Total_Inventory_Value_USD"
]

for col in money_columns:
    df[col] = (
        df[col]
        .str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# -------------------------
# AVAILABLE STOCK
# -------------------------

df["Available_Stock"] = (
    df["Quantity_On_Hand"]
    - df["Quantity_Reserved"]
    - df["Quantity_Committed"]
)

# -------------------------
# DAYS TO EXPIRY
# -------------------------

today = pd.Timestamp.today().normalize()

df["Days_to_Expiry"] = (
    df["Expiry_Date"] - today
).dt.days

# -------------------------
# LOW STOCK FLAG
# -------------------------

df["Low_Stock_Flag"] = (
    df["Available_Stock"]
    < df["Reorder_Point"]
)

# -------------------------
# EXPIRY RISK
# -------------------------

def expiry_risk(days):

    if days < 0:
        return "Expired"

    elif days <= 30:
        return "High"

    elif days <= 90:
        return "Medium"

    else:
        return "Low"

df["Expiry_Risk"] = df["Days_to_Expiry"].apply(expiry_risk)

# -------------------------
# SUPPLY RISK SCORE
# -------------------------

def supply_score(row):

    score = 0

    if row["Low_Stock_Flag"]:
        score += 40

    if row["Supplier_OnTime_Pct"] < 80:
        score += 30

    if row["Days_to_Expiry"] < 30:
        score += 30

    return score

df["Supply_Risk_Score"] = df.apply(
    supply_score,
    axis=1
)

# -------------------------
# RISK LEVEL
# -------------------------

def risk_level(score):

    if score >= 70:
        return "High"

    elif score >= 40:
        return "Medium"

    else:
        return "Low"

df["Risk_Level"] = df["Supply_Risk_Score"].apply(risk_level)
# -------------------------
# INVENTORY HEALTH
# -------------------------

def inventory_health(row):

    if row["Available_Stock"] < row["Reorder_Point"]:
        return "Critical"

    elif row["Available_Stock"] > row["Reorder_Point"] * 2:
        return "Overstock"

    else:
        return "Healthy"

df["Inventory_Health"] = df.apply(
    inventory_health,
    axis=1
)

# -------------------------
# SUPPLIER PERFORMANCE
# -------------------------

def supplier_performance(value):

    if value >= 95:
        return "Excellent"

    elif value >= 80:
        return "Good"

    else:
        return "Poor"

df["Supplier_Performance"] = df[
    "Supplier_OnTime_Pct"
].apply(supplier_performance)

# -------------------------
# EXPIRY STATUS
# -------------------------

def expiry_status(days):

    if days < 0:
        return "Expired"

    elif days <= 30:
        return "Near Expiry"

    else:
        return "Safe"

df["Expiry_Status"] = df[
    "Days_to_Expiry"
].apply(expiry_status)

# -------------------------
# STOCK STATUS
# -------------------------

def stock_status(stock):

    if stock < 50:
        return "Low"

    elif stock > 300:
        return "Overstock"

    else:
        return "Normal"

df["Stock_Status"] = df[
    "Available_Stock"
].apply(stock_status)

# -------------------------
# INVENTORY VALUE CATEGORY
# -------------------------

def inventory_value(value):

    if value >= 50000:
        return "High"

    elif value >= 10000:
        return "Medium"

    else:
        return "Low"

df["Inventory_Value_Category"] = df[
    "Total_Inventory_Value_USD"
].apply(inventory_value)

# -------------------------
# SAVE FINAL DATASET
# -------------------------

df.to_csv(
    "outputs/final_inventory.csv",
    index=False
)

# -------------------------
# PROJECT SUMMARY
# -------------------------

print("\n======================================")
print("PROJECT COMPLETED SUCCESSFULLY")
print("======================================")

print("\nDataset Shape:")
print(df.shape)

print("\nTotal Columns:")
print(len(df.columns))

print("\nNew Columns Created:")

new_columns = [
    "Available_Stock",
    "Days_to_Expiry",
    "Low_Stock_Flag",
    "Expiry_Risk",
    "Supply_Risk_Score",
    "Risk_Level",
    "Inventory_Health",
    "Supplier_Performance",
    "Expiry_Status",
    "Stock_Status",
    "Inventory_Value_Category"
]

for column in new_columns:
    print("✓", column)

print("\nFinal Dataset Saved Successfully!")

print("\nPreview:")

print(
    df[
        [
            "SKU_Name",
            "Available_Stock",
            "Days_to_Expiry",
            "Supplier_OnTime_Pct",
            "Supply_Risk_Score",
            "Risk_Level",
            "Inventory_Health",
            "Supplier_Performance",
            "Expiry_Status",
            "Stock_Status",
            "Inventory_Value_Category"
        ]
    ].head()
)