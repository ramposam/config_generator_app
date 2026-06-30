# Multi-Agent Database Query System

This system provides intelligent agents for querying E-commerce, Football, and IPL Cricket databases with comprehensive schema documentation.

## Overview

### Components

1. **ecommerce_agent.py**: Handles queries on the E-commerce database (ECOMMERCE_DB.SILVER schema)
2. **football_agent.py**: Handles queries on the Football database (ETL_PIPELINES_DB.public schema)
3. **ipl_agent.py**: Handles queries on the IPL Cricket database (ETL_PIPELINES_DB.SILVER schema)
4. **ecommerce_agent.md**: Complete schema documentation for E-commerce database
5. **football_agent.md**: Complete schema documentation for Football database
6. **ipl_agent.md**: Complete schema documentation for IPL Cricket database

## Schema Documentation Files

Each agent has a corresponding `.md` file containing:
- **Database Connection Details**: Database name, schema name, and available tables
- **Table Schemas**: Column names, data types, nullable constraints, and descriptions
- **Sample Values**: Example data to understand data types and patterns
- **Example Queries**: Common SQL patterns for typical analyses
- **Important SQL Rules**: Formatting requirements and best practices
- **Common Analysis Patterns**: Pre-built query patterns for frequent use cases

### Why Schema Documentation?

The schema documentation files serve as the knowledge base for the agents:
- **Prevents Database Queries for Schema Info**: No need to query the database every time for schema information
- **Improves Query Generation**: LLM has complete understanding of table structure and relationships
- **Consistent Formatting**: Ensures proper SQL syntax (double-quoted identifiers)
- **Error Prevention**: Reduces malformed queries that result in API errors
- **Performance**: Faster initialization without hitting the database

## Agent Architecture

### Enhanced Tool Descriptions

Each agent's tools now include detailed schema information in their docstrings:

```python
@tool
def query_ecommerce_database(sql_query: str) -> str:
    """Execute SQL queries on E-commerce database
    
    Available tables: T_STG_ORDERS, T_STG_ORDER_ITEMS, T_STG_PRODUCTS, 
                     T_STG_USERS, T_STG_REVIEWS, T_STG_EVENTS
    
    CRITICAL: Use double quotes around table names:
    - ✅ SELECT * FROM "SILVER"."T_STG_ORDERS"
    - ❌ SELECT * FROM SILVER.T_STG_ORDERS
    """
```

### Schema Loading

Agents now load their schema documentation at initialization:

```python
def load_ecommerce_schema() -> str:
    """Load E-commerce database schema from markdown file"""
    schema_path = Path(__file__).parent / "ecommerce_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r') as f:
            return f.read()
    return "Schema documentation not found"
```

The loaded schema is available for debugging and logging.

## Key Improvements

### 1. **Proper Schema Understanding**
- Agents now have complete knowledge of table structures
- Column names, data types, and relationships are documented
- Sample values show data patterns (e.g., revenue amounts, date formats)

### 2. **Correct SQL Generation**
- Tool descriptions emphasize proper quoting rules
- Example queries show correct JOIN patterns
- Common mistakes are explicitly called out

### 3. **Query Examples**
- Revenue Analysis examples show proper use of T_STG_ORDER_ITEMS
- Customer Analysis examples demonstrate correct JOINs
- Product Performance examples show aggregate functions with proper GROUP BY

### 4. **Error Prevention**
Example from previous error - WRONG:
```sql
-- ❌ WRONG - unit_price * quantity calculation
SELECT SUM(oi.unit_price * oi.quantity) AS total_revenue 
FROM SILVER.T_STG_ORDER_ITEMS oi
```

Fixed version:
```sql
-- ✅ CORRECT - use pre-calculated total_price
SELECT SUM(oi.total_price) as total_revenue 
FROM "SILVER"."T_STG_ORDER_ITEMS" oi
```

## Usage

### Using E-commerce Agent

```python
from agents import create_ecommerce_agent

# Create agent
agent = create_ecommerce_agent(use_groq=False)

# Execute query
result = agent.invoke({
    "messages": [{"role": "user", "content": "What is total revenue?"}]
})
```

### Using IPL Agent

```python
from agents import create_ipl_agent

# Create agent
agent = create_ipl_agent(use_groq=False)

# Execute query
result = agent.invoke({
    "messages": [{"role": "user", "content": "Show top run scorers in IPL 2024"}]
})
```

### Using Football Agent

```python
from agents import create_football_agent

# Create agent
agent = create_football_agent(use_groq=False)

# Execute query
result = agent.invoke({
    "messages": [{"role": "user", "content": "Show top rated players"}]
})
```

## Updating Schema Documentation

If your database schema changes, update the corresponding `.md` file:

1. **E-commerce**: Edit `ecommerce_agent.md`
   - Update table definitions
   - Add/remove columns
   - Provide new sample values
   - Add new example queries

2. **Football**: Edit `football_agent.md`
   - Update table definitions
   - Add/remove columns
   - Provide new sample values
   - Add new example queries

3. **IPL Cricket**: Edit `ipl_agent.md`
   - Update table definitions
   - Add/remove columns
   - Provide new sample values
   - Add new example queries

### Schema Update Format

```markdown
### 1. TABLE_NAME
**Description**: What this table contains

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| column_id | integer | NO | Primary key description |
| column_name | varchar | YES | Purpose of this column |

**Sample Values**:
```
column_name: "value1", "value2"
```

**Example Queries**:
```
```

```sql
-- Describe what this query does
SELECT * FROM "SCHEMA"."TABLE_NAME" WHERE condition;
```

## Common Analysis Patterns

### IPL Season-wise Analysis
```sql
SELECT 
    "SEASON",
    COUNT(DISTINCT "MATCH_ID") as total_matches,
    SUM("RUNS_OF_BAT") as total_runs,
    COUNT("WICKET_TYPE") as total_wickets
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "SEASON"
ORDER BY "SEASON"
```

### IPL Top Batsmen
```sql
SELECT 
    "STRIKER",
    COUNT(*) as balls_faced,
    SUM("RUNS_OF_BAT") as total_runs,
    COUNT(CASE WHEN "RUNS_OF_BAT" = 4 THEN 1 END) as fours,
    COUNT(CASE WHEN "RUNS_OF_BAT" = 6 THEN 1 END) as sixes,
    ROUND(SUM("RUNS_OF_BAT")::numeric / NULLIF(COUNT(*), 0), 2) as strike_rate
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "STRIKER"
ORDER BY total_runs DESC
LIMIT 20
```

### Revenue Analysis
```sql
SELECT 
    SUM(oi.total_price) as total_revenue,
    COUNT(DISTINCT o.order_id) as order_count,
    AVG(oi.total_price) as avg_item_value
FROM "SILVER"."T_STG_ORDERS" o
JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
```

```
```sql
SELECT 
    u.country,
    COUNT(DISTINCT u.user_id) as customer_count,
    SUM(oi.total_price) as total_spent_per_country
FROM "SILVER"."T_STG_USERS" u
LEFT JOIN "SILVER"."T_STG_ORDERS" o ON u.user_id = o.user_id
LEFT JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o.order_id = oi.order_id
GROUP BY u.country
ORDER BY total_spent_per_country DESC
```

### Customer Segmentation
```sql
```sql
SELECT 
    p.player_name,
    p.position,
    pa.overall_rating,
    pa.potential,
    CASE 
        WHEN p.position = 'Forward' THEN pa.shooting
        WHEN p.position = 'Midfielder' THEN pa.passing
        WHEN p.position = 'Defender' THEN pa.defense
        ELSE pa.overall_rating
    END as position_skill
FROM "public"."PLAYER" p
JOIN "public"."PLAYER_ATTRIBUTES" pa ON p.player_id = pa.player_id
ORDER BY pa.overall_rating DESC
LIMIT 20
```

### Player Performance Ranking
```sql

## Troubleshooting
```
### Issue: "table ... does not exist"
```

**Cause**: Table name not quoted or wrong schema name
**Solution**: Use double quotes: `"SCHEMA"."TABLE_NAME"`

### Issue: "Failed to call a function"
**Cause**: Incorrect JOIN syntax or missing GROUP BY with aggregates
**Solution**: Review Example Queries in schema documentation

### Issue: Wrong revenue calculation
**Cause**: Using `unit_price * quantity` instead of `total_price`
**Solution**: Use `T_STG_ORDER_ITEMS.total_price` for accurate revenue

### Issue: IPL query returns no results
**Cause**: Column names not in UPPERCASE or not quoted
**Solution**: Use UPPERCASE column names with double quotes: `"MATCH_ID"`, `"STRIKER"`, `"BOWLER"`

```

```
## File Structure
```
```

multi_agent_app/agents/
├── __init__.py
├── ecommerce_agent.py          # E-commerce agent implementation
├── ecommerce_agent.md          # E-commerce schema documentation
├── football_agent.py           # Football agent implementation
├── football_agent.md           # Football schema documentation
├── ipl_agent.py               # IPL Cricket agent implementation
├── ipl_agent.md               # IPL Cricket schema documentation
├── tavily_agent.py             # Web search agent
├── weather_agent.py            # Weather agent
├── aviation_agent.py           # Aviation agent
└── README.md                   # This file

## Benefits of Schema Documentation Approach
```

1. **No Runtime Database Calls**: Schema info is loaded from markdown, not queried from DB
2. **Faster Agent Initialization**: No schema discovery queries needed
3. **Better Query Generation**: LLM has complete schema context upfront
4. **Consistent Formatting**: All queries use the documented SQL patterns
5. **Easy Maintenance**: Update `.md` files when schema changes
6. **Better Error Messages**: Schema documentation helps agents understand and fix errors
7. **Version Control**: Schema changes are tracked in `.md` files

## Next Steps
```

