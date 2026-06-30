# E-commerce Database Agent

## Database Connection Details
- **Database**: ECOMMERCE_DB
- **Schema**: SILVER
- **Available Tables**: T_STG_ORDERS, T_STG_REVIEWS, T_STG_EVENTS, T_STG_ORDER_ITEMS, T_STG_PRODUCTS, T_STG_USERS

---

## Table Schemas

### 1. SILVER.T_STG_ORDERS
**Description**: Order information and order-level details

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ORDER_ID | text | YES | Primary key, unique identifier for each order |
| USER_ID | text | YES | Foreign key to T_STG_USERS |
| ORDER_DATE | text | YES | Date when the order was placed |
| ORDER_STATUS | text | YES | Order status (pending, completed, cancelled, etc.) |
| TOTAL_AMOUNT | double precision | YES | Total order amount/value |
| CREATED_DTS | timestamp without time zone | YES | Creation timestamp |
| CREATED_BY | text | YES | Created by user |
| UPDATED_DTS | timestamp without time zone | YES | Update timestamp |
| UPDATED_BY | text | YES | Updated by user |
| UNIQUE_HASH_ID | text | YES | Unique hash identifier |
| ROW_HASH_ID | text | YES | Row hash identifier |
| ACTIVE_FL | text | YES | Active flag |
| EFFECTIVE_START_DATE | timestamp without time zone | YES | Effective start date |
| EFFECTIVE_END_DATE | timestamp without time zone | YES | Effective end date |

**Sample Values**:
```
ORDER_ID: "ORD001", "ORD002", "ORD003"
USER_ID: "USER100", "USER101", "USER102"
ORDER_DATE: "2024-01-15 14:30:00"
TOTAL_AMOUNT: 150.99, 250.50, 75.00
ORDER_STATUS: completed, pending, cancelled
```

**Example Queries**:
```sql
-- Total revenue from all completed orders
SELECT SUM("TOTAL_AMOUNT") as total_revenue FROM "SILVER"."T_STG_ORDERS" 
WHERE "ORDER_STATUS" = 'completed';

-- Number of orders per user
SELECT "USER_ID", COUNT(*) as order_count 
FROM "SILVER"."T_STG_ORDERS" 
GROUP BY "USER_ID";

-- Average order value
SELECT AVG("TOTAL_AMOUNT") as avg_order_value FROM "SILVER"."T_STG_ORDERS";
```

---

### 2. SILVER.T_STG_ORDER_ITEMS
**Description**: Line items in each order (product details per order)

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ORDER_ITEM_ID | text | YES | Primary key |
| ORDER_ID | text | YES | Foreign key to T_STG_ORDERS |
| PRODUCT_ID | text | YES | Foreign key to T_STG_PRODUCTS |
| USER_ID | text | YES | Foreign key to T_STG_USERS |
| QUANTITY | numeric | YES | Number of items ordered |
| ITEM_PRICE | double precision | YES | Price per unit at time of order |
| ITEM_TOTAL | double precision | YES | quantity * unit_price |
| CREATED_DTS | timestamp without time zone | YES | Creation timestamp |
| CREATED_BY | text | YES | Created by user |
| UPDATED_DTS | timestamp without time zone | YES | Update timestamp |
| UPDATED_BY | text | YES | Updated by user |
| UNIQUE_HASH_ID | text | YES | Unique hash identifier |
| ROW_HASH_ID | text | YES | Row hash identifier |
| ACTIVE_FL | text | YES | Active flag |
| EFFECTIVE_START_DATE | timestamp without time zone | YES | Effective start date |
| EFFECTIVE_END_DATE | timestamp without time zone | YES | Effective end date |

**Sample Values**:
```
QUANTITY: 1, 2, 5, 10
ITEM_PRICE: 25.99, 49.50, 100.00
ITEM_TOTAL: 25.99, 99.00, 500.00
```

**Example Queries**:
```sql
-- Total revenue from all order items
SELECT SUM("ITEM_TOTAL") as total_revenue FROM "SILVER"."T_STG_ORDER_ITEMS";

-- Total quantity sold per product
SELECT "PRODUCT_ID", SUM("QUANTITY") as total_qty 
FROM "SILVER"."T_STG_ORDER_ITEMS" 
GROUP BY "PRODUCT_ID";

-- Join with orders to get order-level details
SELECT o."ORDER_ID", oi."PRODUCT_ID", oi."QUANTITY", oi."ITEM_PRICE", oi."ITEM_TOTAL"
FROM "SILVER"."T_STG_ORDERS" o
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."ORDER_ID" = oi."ORDER_ID";
```

---

### 3. SILVER.T_STG_PRODUCTS
**Description**: Product catalog information

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| PRODUCT_ID | text | YES | Primary key |
| PRODUCT_NAME | text | YES | Name of the product |
| CATEGORY | text | YES | Product category |
| BRAND | text | YES | Product brand |
| PRICE | double precision | YES | Standard product price |
| RATING | double precision | YES | Product rating |
| CREATED_DTS | timestamp without time zone | YES | Creation timestamp |
| CREATED_BY | text | YES | Created by user |
| UPDATED_DTS | timestamp without time zone | YES | Update timestamp |
| UPDATED_BY | text | YES | Updated by user |
| UNIQUE_HASH_ID | text | YES | Unique hash identifier |
| ROW_HASH_ID | text | YES | Row hash identifier |
| ACTIVE_FL | text | YES | Active flag |
| EFFECTIVE_START_DATE | timestamp without time zone | YES | Effective start date |
| EFFECTIVE_END_DATE | timestamp without time zone | YES | Effective end date |

**Sample Values**:
```
PRODUCT_NAME: "Laptop", "Mouse", "Keyboard"
CATEGORY: "Electronics", "Accessories"
PRICE: 999.99, 25.99, 75.50
```

**Example Queries**:
```sql
-- All products by category
SELECT * FROM "SILVER"."T_STG_PRODUCTS" WHERE "CATEGORY" = 'Electronics';

-- Product count by category
SELECT "CATEGORY", COUNT(*) as product_count 
FROM "SILVER"."T_STG_PRODUCTS" 
GROUP BY "CATEGORY";
```

---

### 4. SILVER.T_STG_USERS
**Description**: Customer/user information

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| USER_ID | text | YES | Primary key |
| NAME | text | YES | User's name |
| EMAIL | text | YES | User's email address |
| GENDER | text | YES | User's gender |
| CITY | text | YES | User's city |
| SIGNUP_DATE | text | YES | Date user signed up |
| CREATED_DTS | timestamp without time zone | YES | Creation timestamp |
| CREATED_BY | text | YES | Created by user |
| UPDATED_DTS | timestamp without time zone | YES | Update timestamp |
| UPDATED_BY | text | YES | Updated by user |
| UNIQUE_HASH_ID | text | YES | Unique hash identifier |
| ROW_HASH_ID | text | YES | Row hash identifier |
| ACTIVE_FL | text | YES | Active flag |
| EFFECTIVE_START_DATE | timestamp without time zone | YES | Effective start date |
| EFFECTIVE_END_DATE | timestamp without time zone | YES | Effective end date |

**Sample Values**:
```
NAME: "John Doe", "Jane Smith"
EMAIL: "john@example.com"
CITY: "New York", "London", "Toronto"
```

**Example Queries**:
```sql
-- User count by city
SELECT "CITY", COUNT(*) as user_count 
FROM "SILVER"."T_STG_USERS" 
GROUP BY "CITY";

-- All users
SELECT * FROM "SILVER"."T_STG_USERS";
```

---

### 5. SILVER.T_STG_REVIEWS
**Description**: Product reviews from customers

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| REVIEW_ID | text | YES | Primary key |
| ORDER_ID | text | YES | Foreign key to T_STG_ORDERS |
| PRODUCT_ID | text | YES | Foreign key to T_STG_PRODUCTS |
| USER_ID | text | YES | Foreign key to T_STG_USERS |
| RATING | numeric | YES | Rating 1-5 |
| REVIEW_TEXT | text | YES | Review content |
| REVIEW_DATE | text | YES | Date of review |
| CREATED_DTS | timestamp without time zone | YES | Creation timestamp |
| CREATED_BY | text | YES | Created by user |
| UPDATED_DTS | timestamp without time zone | YES | Update timestamp |
| UPDATED_BY | text | YES | Updated by user |
| UNIQUE_HASH_ID | text | YES | Unique hash identifier |
| ROW_HASH_ID | text | YES | Row hash identifier |
| ACTIVE_FL | text | YES | Active flag |
| EFFECTIVE_START_DATE | timestamp without time zone | YES | Effective start date |
| EFFECTIVE_END_DATE | timestamp without time zone | YES | Effective end date |

**Sample Values**:
```
RATING: 1, 2, 3, 4, 5
REVIEW_TEXT: "Great product!", "Poor quality"
```

**Example Queries**:
```sql
-- Average rating per product
SELECT "PRODUCT_ID", AVG("RATING") as avg_rating, COUNT(*) as review_count
FROM "SILVER"."T_STG_REVIEWS"
GROUP BY "PRODUCT_ID";

-- Highly rated products (4+ stars)
SELECT "PRODUCT_ID", AVG("RATING") as avg_rating
FROM "SILVER"."T_STG_REVIEWS"
GROUP BY "PRODUCT_ID"
HAVING AVG("RATING") >= 4;
```

---

### 6. SILVER.T_STG_EVENTS
**Description**: User activity/event tracking

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| EVENT_ID | text | YES | Primary key |
| USER_ID | text | YES | Foreign key to T_STG_USERS |
| PRODUCT_ID | text | YES | Foreign key to T_STG_PRODUCTS |
| EVENT_TYPE | text | YES | Type: view, click, purchase, add_to_cart |
| EVENT_TIMESTAMP | text | YES | Date and time of event |
| CREATED_DTS | timestamp without time zone | YES | Creation timestamp |
| CREATED_BY | text | YES | Created by user |
| UPDATED_DTS | timestamp without time zone | YES | Update timestamp |
| UPDATED_BY | text | YES | Updated by user |
| UNIQUE_HASH_ID | text | YES | Unique hash identifier |
| ROW_HASH_ID | text | YES | Row hash identifier |
| ACTIVE_FL | text | YES | Active flag |
| EFFECTIVE_START_DATE | timestamp without time zone | YES | Effective start date |
| EFFECTIVE_END_DATE | timestamp without time zone | YES | Effective end date |

**Sample Values**:
```
EVENT_TYPE: "view", "click", "purchase", "add_to_cart"
```

**Example Queries**:
```sql
-- Event count by type
SELECT "EVENT_TYPE", COUNT(*) as event_count
FROM "SILVER"."T_STG_EVENTS"
GROUP BY "EVENT_TYPE";

-- User's purchase history
SELECT * FROM "SILVER"."T_STG_EVENTS" 
WHERE "USER_ID" = '100' AND "EVENT_TYPE" = 'purchase';
```

---

## Important SQL Rules

1. **ALWAYS wrap ALL identifiers in double quotes - schemas, tables, AND columns**
   - ✅ CORRECT: `SELECT "total_price" FROM "SILVER"."T_STG_ORDER_ITEMS"`
   - ✅ CORRECT: `SELECT SUM("total_price") FROM "SILVER"."T_STG_ORDER_ITEMS"`
   - ✅ CORRECT: `SELECT "order_id", "amount" FROM "SILVER"."T_STG_ORDERS"`
   - ✅ CORRECT: `SELECT "TOTAL_PRICE" FROM "SILVER"."T_STG_ORDER_ITEMS"` (if column is uppercase)
   - ❌ WRONG: `SELECT * FROM SILVER.T_STG_ORDERS`
   - ❌ WRONG: `SELECT total_price FROM "SILVER"."T_STG_ORDER_ITEMS"` (column not quoted)
   - ❌ WRONG: `SELECT SUM(total_price) FROM "SILVER"."T_STG_ORDER_ITEMS"` (column not quoted)
   - Note: Use the EXACT case as defined in the database schema

2. **Use proper table aliases with quoted column names**
   - ✅ CORRECT: `SELECT o."order_id", oi."total_price" FROM "SILVER"."T_STG_ORDERS" o JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."order_id" = oi."order_id"`
   - ❌ WRONG: `SELECT o.order_id FROM SILVER.T_STG_ORDERS o`

3. **Always include JOINs** when combining data from multiple tables

4. **Use proper GROUP BY** clauses when using aggregate functions

5. **String values in WHERE** use single quotes:
   - ✅ CORRECT: `WHERE "status" = 'completed'`
   - ❌ WRONG: `WHERE status = 'completed'`

## Common Analysis Patterns

### Revenue Analysis
```sql
SELECT 
    DATE_TRUNC('month', TO_TIMESTAMP(o."ORDER_DATE", 'YYYY-MM-DD HH24:MI:SS')) as month,
    SUM(oi."ITEM_TOTAL") as monthly_revenue,
    COUNT(DISTINCT o."ORDER_ID") as order_count,
    AVG(oi."ITEM_TOTAL") as avg_item_value
FROM "SILVER"."T_STG_ORDERS" o
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."ORDER_ID" = oi."ORDER_ID"
WHERE o."ORDER_STATUS" = 'completed'
GROUP BY DATE_TRUNC('month', TO_TIMESTAMP(o."ORDER_DATE", 'YYYY-MM-DD HH24:MI:SS'))
ORDER BY month DESC;
```

### Customer Analysis
```sql
SELECT 
    u."USER_ID",
    u."NAME",
    u."CITY",
    COUNT(DISTINCT o."ORDER_ID") as total_orders,
    SUM(oi."ITEM_TOTAL") as total_spent,
    AVG(oi."ITEM_TOTAL") as avg_order_value
FROM "SILVER"."T_STG_USERS" u
LEFT JOIN "SILVER"."T_STG_ORDERS" o ON u."USER_ID" = o."USER_ID"
LEFT JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."ORDER_ID" = oi."ORDER_ID"
GROUP BY u."USER_ID", u."NAME", u."CITY";
```

### Product Performance
```sql
SELECT 
    p."PRODUCT_ID",
    p."PRODUCT_NAME",
    p."CATEGORY",
    COUNT(oi."ORDER_ITEM_ID") as units_sold,
    SUM(oi."ITEM_TOTAL") as total_revenue,
    AVG(r."RATING") as avg_rating,
    COUNT(DISTINCT r."REVIEW_ID") as review_count
FROM "SILVER"."T_STG_PRODUCTS" p
LEFT JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON p."PRODUCT_ID" = oi."PRODUCT_ID"
LEFT JOIN "SILVER"."T_STG_REVIEWS" r ON p."PRODUCT_ID" = r."PRODUCT_ID"
GROUP BY p."PRODUCT_ID", p."PRODUCT_NAME", p."CATEGORY";
```

