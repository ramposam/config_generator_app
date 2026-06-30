# Football Database Agent - SQL Guide

## CRITICAL: SQL Formatting Rules

**ALL identifiers MUST use double quotes with EXACT CASE:**

### Rule 1: Quote EVERYTHING
- ✅ `SELECT "column_name" FROM "public"."TABLE"`
- ❌ `SELECT column_name FROM public.TABLE`

### Rule 2: Use exact column names (case-sensitive in quotes)
- ✅ `SELECT "overall_rating" FROM "public"."PLAYER_ATTRIBUTES"` (if column is lowercase)
- ✅ `SELECT "OVERALL_RATING" FROM "public"."PLAYER_ATTRIBUTES"` (if column is uppercase)
- ✅ `SELECT "buildUpPlaySpeed" FROM "public"."TEAM_ATTRIBUTES"` (if column is camelCase)
- Note: Use the EXACT case as defined in the database schema

### Rule 3: Quote columns in all clauses
- ✅ `WHERE "position" = 'Forward'`
- ✅ `GROUP BY "nationality"`
- ✅ `ON p."player_id" = pa."player_id"`

### Rule 4: Aggregate functions need quoted columns
- ✅ `SUM("home_team_goal")`
- ✅ `AVG("overall_rating")`
- ✅ `COUNT(DISTINCT "player_id")`
- ❌ `SUM(home_team_goal)` - MISSING QUOTES

---

## Database Connection Details
- **Database**: ETL_PIPELINES_DB
- **Schema**: public
- **Available Tables**: PLAYER, MATCH, LEAGUE, TEAM, COUNTRY, TEAM_ATTRIBUTES, PLAYER_ATTRIBUTES

---

## Table Schemas with Exact Column Names

### 1. "public"."PLAYER"
**Description**: Player information and details

Column Names (use EXACT case in double quotes):
- "player_id" (integer) - Primary key
- "player_name" (varchar) - Name
- "nationality" (varchar) - Nationality
- "height" (decimal) - Height in cm
- "weight" (integer) - Weight in kg
- "birth_date" (date) - Date of birth
- "position" (varchar) - Position (Goalkeeper, Defender, Midfielder, Forward)

**Example Queries**:
```sql
-- Total players
SELECT COUNT(*) as total_players FROM "public"."PLAYER";

-- Players by nationality
SELECT "nationality", COUNT(*) as player_count 
FROM "public"."PLAYER" 
GROUP BY "nationality";

-- Players by position
SELECT "position", COUNT(*) as count
FROM "public"."PLAYER"
GROUP BY "position";
```

---

### 2. "public"."MATCH"
**Description**: Football match results and details

Column Names (use EXACT case in double quotes):
- "match_id" (integer) - Primary key
- "league_id" (integer) - Foreign key to LEAGUE
- "home_team_id" (integer) - Foreign key to TEAM (home)
- "away_team_id" (integer) - Foreign key to TEAM (away)
- "home_team_goal" (integer) - Goals by home team
- "away_team_goal" (integer) - Goals by away team
- "match_date" (date) - Date of match
- "season" (varchar) - Season (e.g., '2023-2024')

**Example Queries**:
```sql
-- Total matches
SELECT COUNT(*) as total_matches FROM "public"."MATCH";

-- Match statistics
SELECT 
    COUNT(*) as total_matches,
    SUM(CASE WHEN "home_team_goal" > "away_team_goal" THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN "home_team_goal" < "away_team_goal" THEN 1 ELSE 0 END) as away_wins,
    SUM(CASE WHEN "home_team_goal" = "away_team_goal" THEN 1 ELSE 0 END) as draws
FROM "public"."MATCH";

-- Highest scoring matches
SELECT * FROM "public"."MATCH" 
ORDER BY ("home_team_goal" + "away_team_goal") DESC 
LIMIT 10;
```

---

### 3. "public"."TEAM"
**Description**: Football team information

Column Names (use EXACT case in double quotes):
- "team_id" (integer) - Primary key
- "team_short_name" (varchar) - Abbreviation
- "team_long_name" (varchar) - Full name
- "team_api_id" (integer) - API identifier

**Example Queries**:
```sql
-- All teams
SELECT COUNT(*) as total_teams FROM "public"."TEAM";

-- Find team
SELECT * FROM "public"."TEAM" 
WHERE "team_long_name" LIKE '%Manchester%';
```

---

### 4. "public"."LEAGUE"
**Description**: Football league information

Column Names (use EXACT case in double quotes):
- "league_id" (integer) - Primary key
- "league_name" (varchar) - Name
- "country_id" (integer) - Foreign key to COUNTRY

**Example Queries**:
```sql
-- All leagues
SELECT COUNT(*) as total_leagues FROM "public"."LEAGUE";

-- Leagues by country
SELECT "country_id", COUNT(*) as league_count 
FROM "public"."LEAGUE" 
GROUP BY "country_id";
```

---

### 5. "public"."COUNTRY"
**Description**: Country information

Column Names (use EXACT case in double quotes):
- "country_id" (integer) - Primary key
- "country_name" (varchar) - Name

**Example Queries**:
```sql
-- All countries
SELECT COUNT(*) as total_countries FROM "public"."COUNTRY";

-- Countries with leagues
SELECT c."country_name", COUNT(DISTINCT l."league_id") as league_count
FROM "public"."COUNTRY" c
LEFT JOIN "public"."LEAGUE" l ON c."country_id" = l."country_id"
GROUP BY c."country_name";
```

---

### 6. "public"."PLAYER_ATTRIBUTES"
**Description**: Player performance attributes and ratings

Column Names (use EXACT case in double quotes):
- "player_attributes_id" (integer) - Primary key
- "player_id" (integer) - Foreign key to PLAYER
- "overall_rating" (integer) - Overall rating (1-100)
- "potential" (integer) - Potential rating (1-100)
- "pace" (integer) - Pace attribute
- "shooting" (integer) - Shooting attribute
- "passing" (integer) - Passing attribute
- "dribbling" (integer) - Dribbling attribute
- "defense" (integer) - Defense attribute
- "physical" (integer) - Physical attribute
- "date_from" (date) - Date from which attributes are valid

**Example Queries**:
```sql
-- Top rated players
SELECT p."player_name", pa."overall_rating", pa."potential"
FROM "public"."PLAYER" p
JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."player_id" = pa."player_id"
ORDER BY pa."overall_rating" DESC
LIMIT 20;

-- Average attributes by position
SELECT p."position", AVG(pa."overall_rating") as avg_rating
FROM "public"."PLAYER" p
JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."player_id" = pa."player_id"
GROUP BY p."position";
```

---

### 7. "public"."TEAM_ATTRIBUTES"
**Description**: Team performance attributes and ratings

Column Names (use EXACT case in double quotes - NOTE camelCase):
- "team_attributes_id" (integer) - Primary key
- "team_id" (integer) - Foreign key to TEAM
- "buildUpPlaySpeed" (integer) - Build-up play speed (camelCase!)
- "buildUpPlayPassing" (varchar) - Build-up play style
- "chanceCreationPassing" (varchar) - Chance creation style
- "defenseAggression" (integer) - Defense aggression (camelCase!)
- "defenseTeamWidth" (integer) - Team width (camelCase!)
- "date_from" (date) - Date from valid

**Example Queries**:
```sql
-- Team attributes
SELECT * FROM "public"."TEAM_ATTRIBUTES" 
WHERE "team_id" = 1;

-- Teams with aggressive defense
SELECT t."team_long_name", ta."defenseAggression"
FROM "public"."TEAM" t
JOIN "public"."TEAM_ATTRIBUTES" ta ON t."team_id" = ta."team_id"
WHERE ta."defenseAggression" > 75
ORDER BY ta."defenseAggression" DESC;
```

---

## Complex Query Examples with Proper Quoting

### Match Statistics by League
```sql
SELECT 
    l."league_name",
    c."country_name",
    COUNT(m."match_id") as total_matches,
    SUM(CASE WHEN m."home_team_goal" > m."away_team_goal" THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN m."home_team_goal" < m."away_team_goal" THEN 1 ELSE 0 END) as away_wins,
    SUM(CASE WHEN m."home_team_goal" = m."away_team_goal" THEN 1 ELSE 0 END) as draws,
    AVG(m."home_team_goal" + m."away_team_goal") as avg_goals_per_match
FROM "public"."MATCH" m
JOIN "public"."LEAGUE" l ON m."league_id" = l."league_id"
JOIN "public"."COUNTRY" c ON l."country_id" = c."country_id"
GROUP BY l."league_name", c."country_name";
```

### Team Performance
```sql
SELECT 
    t."team_long_name",
    COUNT(CASE WHEN m."home_team_id" = t."team_id" THEN 1 END) as home_matches,
    SUM(CASE WHEN m."home_team_id" = t."team_id" AND m."home_team_goal" > m."away_team_goal" THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN m."away_team_id" = t."team_id" AND m."away_team_goal" > m."home_team_goal" THEN 1 ELSE 0 END) as away_wins
FROM "public"."TEAM" t
LEFT JOIN "public"."MATCH" m ON (m."home_team_id" = t."team_id" OR m."away_team_id" = t."team_id")
GROUP BY t."team_long_name";
```

### Top Performers by Position
```sql
SELECT 
    p."position",
    p."player_name",
    p."nationality",
    pa."overall_rating",
    CASE 
        WHEN p."position" = 'Goalkeeper' THEN pa."defense"
        WHEN p."position" = 'Defender' THEN pa."defense"
        WHEN p."position" = 'Midfielder' THEN pa."passing"
        WHEN p."position" = 'Forward' THEN pa."shooting"
    END as position_skill
FROM "public"."PLAYER" p
JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."player_id" = pa."player_id"
ORDER BY pa."overall_rating" DESC;
```

---

## Common Mistakes to AVOID

❌ **WRONG**: Missing quotes on columns
```sql
SELECT overall_rating FROM public.PLAYER_ATTRIBUTES  -- WRONG!
```

❌ **WRONG**: Wrong case in quotes (case must match database definition)
```sql
-- If column is defined as "buildUpPlaySpeed" in database:
SELECT "BuildUpPlaySpeed" FROM "public"."TEAM_ATTRIBUTES"  -- WRONG (case mismatch)
-- If column is defined as "OVERALL_RATING" in database:
SELECT "overall_rating" FROM "public"."PLAYER_ATTRIBUTES"  -- WRONG (case mismatch)
```

❌ **WRONG**: Mixing quoted and unquoted
```sql
SELECT "overall_rating" FROM public.PLAYER  -- WRONG (schema/table not quoted)
```

❌ **WRONG**: Missing quotes in JOINs
```sql
SELECT * FROM TEAM t JOIN MATCH m ON t.team_id = m.home_team_id  -- WRONG
```

---

## ✅ CORRECT Examples Summary

- ✅ `SELECT "overall_rating" FROM "public"."PLAYER_ATTRIBUTES"`
- ✅ `SELECT "buildUpPlaySpeed" FROM "public"."TEAM_ATTRIBUTES"` (camelCase!)
- ✅ `WHERE "position" = 'Forward'`
- ✅ `GROUP BY "position"`
- ✅ `ON p."player_id" = pa."player_id"`
- ✅ `SUM(CASE WHEN "home_team_goal" > "away_team_goal" THEN 1 ELSE 0 END)`


