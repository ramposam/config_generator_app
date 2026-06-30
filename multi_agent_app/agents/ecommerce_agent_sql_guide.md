# E-commerce Database Agent - SQL Guide

## CRITICAL: SQL Formatting Rules

**ALL identifiers MUST use double quotes with EXACT CASE:**

### Rule 1: Quote EVERYTHING
- ✅ `SELECT "column_name" FROM "SCHEMA"."TABLE"`
- ❌ `SELECT column_name FROM SCHEMA.TABLE`
- ❌ `SELECT total_price FROM SILVER.T_STG_ORDER_ITEMS`

### Rule 2: Use exact column names (case-sensitive in quotes)
- ✅ `SELECT "total_price" FROM "SILVER"."T_STG_ORDER_ITEMS"` (if column is lowercase)
- ✅ `SELECT "TOTAL_PRICE" FROM "SILVER"."T_STG_ORDER_ITEMS"` (if column is uppercase)
- ✅ `SELECT "Total_Price" FROM "SILVER"."T_STG_ORDER_ITEMS"` (if column is mixed case)
- Note: Use the EXACT case as defined in the database schema

### Rule 3: Quote columns in all clauses
- ✅ `WHERE "status" = 'completed'`
- ✅ `GROUP BY "category"`
- ✅ `ORDER BY "total_price" DESC`
- ✅ `ON o."order_id" = oi."order_id"`

### Rule 4: Aggregate functions need quoted columns
- ✅ `SUM("total_price")`
- ✅ `AVG("amount")`
- ✅ `COUNT(DISTINCT "user_id")`
- ❌ `SUM(total_price)` - MISSING QUOTES
- ❌ `AVG(amount)` - MISSING QUOTES

---

## Database Connection Details
- **Database**: ECOMMERCE_DB
- **Schema**: SILVER
- **Available Tables**: T_STG_ORDERS, T_STG_REVIEWS, T_STG_EVENTS, T_STG_ORDER_ITEMS, T_STG_PRODUCTS, T_STG_USERS

---

## Table Schemas with Exact Column Names

### 1. "SILVER"."T_STG_ORDERS"
**Description**: Order information and order-level details

Column Names (use EXACT case in double quotes):
- "order_id" (integer) - Primary key
- "user_id" (integer) - Foreign key to T_STG_USERS
- "order_date" (timestamp) - Date order was placed
- "amount" (decimal) - Total order amount
- "status" (varchar) - Order status
- "payment_method" (varchar) - Payment method
- "shipping_address" (text) - Shipping address

**Example Queries** (with proper quoting):
```sql
-- Total revenue
SELECT SUM("amount") as total_revenue FROM "SILVER"."T_STG_ORDERS"
WHERE "status" = 'completed';

-- Orders per user
SELECT "user_id", COUNT(*) as order_count 
FROM "SILVER"."T_STG_ORDERS" 
GROUP BY "user_id";

-- Average order value
SELECT AVG("amount") as avg_order_value FROM "SILVER"."T_STG_ORDERS";
```

---

### 2. "SILVER"."T_STG_ORDER_ITEMS"
**Description**: Line items in each order (product details per order)

Column Names (use EXACT case in double quotes):
- "order_item_id" (integer) - Primary key
- "order_id" (integer) - Foreign key to T_STG_ORDERS
- "product_id" (integer) - Foreign key to T_STG_PRODUCTS
- "quantity" (integer) - Number of items ordered
- "unit_price" (decimal) - Price per unit
- "total_price" (decimal) - PRE-CALCULATED (quantity × unit_price)

**CRITICAL**: Use "total_price" field, NOT calculating unit_price × quantity

**Example Queries** (with proper quoting):
```sql
-- Total revenue using pre-calculated total_price
SELECT SUM("total_price") as total_revenue 
FROM "SILVER"."T_STG_ORDER_ITEMS";

-- Revenue per product
SELECT "product_id", SUM("total_price") as revenue 
FROM "SILVER"."T_STG_ORDER_ITEMS" 
GROUP BY "product_id";

-- With orders context
SELECT o."order_id", oi."product_id", oi."quantity", oi."unit_price", oi."total_price"
FROM "SILVER"."T_STG_ORDERS" o
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."order_id" = oi."order_id";
```

---

### 3. "SILVER"."T_STG_PRODUCTS"
**Description**: Product catalog information

Column Names (use EXACT case in double quotes):
- "product_id" (integer) - Primary key
- "product_name" (varchar) - Name
- "category" (varchar) - Category
- "price" (decimal) - Standard price
- "description" (text) - Description
- "stock_quantity" (integer) - Stock
- "created_date" (timestamp) - Created date

**Example Queries**:
```sql
-- Products by category
SELECT "category", COUNT(*) as product_count 
FROM "SILVER"."T_STG_PRODUCTS" 
GROUP BY "category";

-- Top products by revenue
SELECT p."product_id", p."product_name", SUM(oi."total_price") as revenue
FROM "SILVER"."T_STG_PRODUCTS" p
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON p."product_id" = oi."product_id"
GROUP BY p."product_id", p."product_name"
ORDER BY revenue DESC;
```

---

### 4. "SILVER"."T_STG_USERS"
**Description**: Customer/user information

Column Names (use EXACT case in double quotes):
- "user_id" (integer) - Primary key
- "user_name" (varchar) - Name
- "email" (varchar) - Email
- "country" (varchar) - Country
- "registration_date" (timestamp) - Registration date
- "user_type" (varchar) - Type (regular, premium, vip)

**Example Queries**:
```sql
-- Users by country
SELECT "country", COUNT(*) as user_count 
FROM "SILVER"."T_STG_USERS" 
GROUP BY "country";

-- Premium users with spending
SELECT u."user_id", u."user_name", SUM(oi."total_price") as total_spent
FROM "SILVER"."T_STG_USERS" u
JOIN "SILVER"."T_STG_ORDERS" o ON u."user_id" = o."user_id"
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."order_id" = oi."order_id"
WHERE u."user_type" = 'premium'
GROUP BY u."user_id", u."user_name";
```

---

### 5. "SILVER"."T_STG_REVIEWS"
**Description**: Product reviews from customers

Column Names (use EXACT case in double quotes):
- "review_id" (integer) - Primary key
- "product_id" (integer) - Foreign key to T_STG_PRODUCTS
- "user_id" (integer) - Foreign key to T_STG_USERS
- "rating" (integer) - Rating 1-5
- "review_text" (text) - Review content
- "review_date" (timestamp) - Review date

**Example Queries**:
```sql
-- Average rating per product
SELECT "product_id", AVG("rating") as avg_rating, COUNT(*) as review_count
FROM "SILVER"."T_STG_REVIEWS"
GROUP BY "product_id";

-- Highly rated products
SELECT "product_id", AVG("rating") as avg_rating
FROM "SILVER"."T_STG_REVIEWS"
GROUP BY "product_id"
HAVING AVG("rating") >= 4;
```

---

### 6. "SILVER"."T_STG_EVENTS"
**Description**: User activity/event tracking

Column Names (use EXACT case in double quotes):
- "event_id" (integer) - Primary key
- "user_id" (integer) - Foreign key to T_STG_USERS
- "event_type" (varchar) - Type (view, click, purchase, add_to_cart)
- "product_id" (integer) - Foreign key to T_STG_PRODUCTS
- "event_date" (timestamp) - Event date/time
- "event_value" (varchar) - Metadata

**Example Queries**:
```sql
-- Events by type
SELECT "event_type", COUNT(*) as event_count
FROM "SILVER"."T_STG_EVENTS"
GROUP BY "event_type";

-- User purchase history
SELECT "user_id", COUNT(*) as purchases
FROM "SILVER"."T_STG_EVENTS" 
WHERE "event_type" = 'purchase'
GROUP BY "user_id";
```

---

## Complex Query Examples with Proper Quoting

### Revenue Analysis
```sql
SELECT 
    DATE_TRUNC('month', o."order_date") as month,
    SUM(oi."total_price") as monthly_revenue,
    COUNT(DISTINCT o."order_id") as order_count,
    AVG(oi."total_price") as avg_item_value
FROM "SILVER"."T_STG_ORDERS" o
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."order_id" = oi."order_id"
WHERE o."status" = 'completed'
GROUP BY DATE_TRUNC('month', o."order_date")
ORDER BY month DESC;
```

### Customer Analysis
```sql
SELECT 
    u."user_id",
    u."user_name",
    u."country",
    COUNT(DISTINCT o."order_id") as total_orders,
    SUM(oi."total_price") as total_spent,
    AVG(oi."total_price") as avg_order_value
FROM "SILVER"."T_STG_USERS" u
LEFT JOIN "SILVER"."T_STG_ORDERS" o ON u."user_id" = o."user_id"
LEFT JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."order_id" = oi."order_id"
GROUP BY u."user_id", u."user_name", u."country";
```

### Product Performance
```sql
SELECT 
    p."product_id",
    p."product_name",
    p."category",
    COUNT(oi."order_item_id") as units_sold,
    SUM(oi."total_price") as total_revenue,
    AVG(r."rating") as avg_rating,
    COUNT(DISTINCT r."review_id") as review_count
FROM "SILVER"."T_STG_PRODUCTS" p
LEFT JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON p."product_id" = oi."product_id"
LEFT JOIN "SILVER"."T_STG_REVIEWS" r ON p."product_id" = r."product_id"
GROUP BY p."product_id", p."product_name", p."category";
```

---

## Common Mistakes to AVOID

❌ **WRONG**: Missing quotes on columns
```sql
SELECT total_price FROM SILVER.T_STG_ORDER_ITEMS  -- WRONG!
```

❌ **WRONG**: Mixing quoted and unquoted
```sql
SELECT "total_price" FROM SILVER.T_STG_ORDER_ITEMS  -- WRONG (schema/table not quoted)
```

❌ **WRONG**: Wrong case in quotes (case must match database definition)
```sql
-- If column is defined as "total_price" in database:
SELECT "Total_Price" FROM "SILVER"."T_STG_ORDER_ITEMS"  -- WRONG (case mismatch)
-- If column is defined as "TOTAL_PRICE" in database:
SELECT "total_price" FROM "SILVER"."T_STG_ORDER_ITEMS"  -- WRONG (case mismatch)
```

❌ **WRONG**: Calculating revenue instead of using total_price
```sql
SELECT SUM("unit_price" * "quantity") FROM "SILVER"."T_STG_ORDER_ITEMS"  -- WRONG (use "total_price" instead)
```

---

## ✅ CORRECT Examples Summary

- ✅ `SELECT "total_price" FROM "SILVER"."T_STG_ORDER_ITEMS"`
- ✅ `SELECT SUM("total_price") as revenue FROM "SILVER"."T_STG_ORDER_ITEMS"`
- ✅ `WHERE "status" = 'completed'`
- ✅ `GROUP BY "category"`
- ✅ `ON o."order_id" = oi."order_id"`
- ✅ `ORDER BY "total_price" DESC`


