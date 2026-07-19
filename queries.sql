-- =====================================================
-- PharmaSupply Guardian SQL Queries
-- =====================================================

-- Query 1: Top 10 Highest Supply Risk Products

SELECT
    SKU_Name,
    Supply_Risk_Score,
    Risk_Level
FROM inventory
ORDER BY Supply_Risk_Score DESC
LIMIT 10;

-- =====================================================
-- Query 2: Find Low Stock Products
-- =====================================================

SELECT
    SKU_Name,
    Available_Stock,
    Reorder_Point
FROM inventory
WHERE Available_Stock < Reorder_Point
ORDER BY Available_Stock ASC;
-- =====================================================
-- Query 3: Find Expired and Near Expiry Products
-- =====================================================

SELECT
    SKU_Name,
    Days_to_Expiry,
    Expiry_Status
FROM inventory
WHERE Days_to_Expiry <= 30
ORDER BY Days_to_Expiry ASC;

-- =====================================================
-- Query 4: High Risk Products
-- =====================================================

SELECT
    SKU_Name,
    Supply_Risk_Score,
    Risk_Level
FROM inventory
WHERE Risk_Level = 'High'
ORDER BY Supply_Risk_Score DESC;