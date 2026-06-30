# IPL Cricket Database Agent

## Database Connection Details
- **Database**: ETL_PIPELINES_DB
- **Schema**: SILVER
- **Available Tables**: T_STG_CRICKET_LEAGUE_IPL_DATA

---

## Table Schemas

### 1. SILVER.T_STG_CRICKET_LEAGUE_IPL_DATA
**Description**: Indian Premier League (IPL) cricket match ball-by-ball data from 2022 to 2026

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| MATCH_ID | numeric | YES | Unique identifier for each match |
| SEASON | numeric | YES | IPL season year (e.g., 2022, 2023, 2024, 2025, 2026) |
| MATCH_NO | numeric | YES | Match number in the season |
| DATE | text | YES | Date of the match |
| VENUE | text | YES | Stadium/venue where match was played |
| BATTING_TEAM | text | YES | Team batting in this ball |
| BOWLING_TEAM | text | YES | Team bowling in this ball |
| INNINGS | numeric | YES | Innings number (1 or 2) |
| OVER | double precision | YES | Over number |
| STRIKER | text | YES | Batsman facing the ball |
| BOWLER | text | YES | Bowler bowling the ball |
| RUNS_OF_BAT | numeric | YES | Runs scored off the bat |
| EXTRAS | numeric | YES | Total extras (wides, no-balls, byes, leg-byes) |
| WIDE | numeric | YES | Wide balls |
| LEGBYES | numeric | YES | Leg byes |
| BYES | numeric | YES | Byes |
| NOBALLS | numeric | YES | No balls |
| WICKET_TYPE | text | YES | Type of wicket (caught, bowled, LBW, run out, etc.) |
| PLAYER_DISMISSED | text | YES | Name of dismissed player |
| FIELDER | text | YES | Name of fielder involved in dismissal |
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
SEASON: 2022, 2023, 2024, 2025, 2026
VENUE: "M Chinnaswamy Stadium", "Wankhede Stadium", "Eden Gardens"
BATTING_TEAM: "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore"
BOWLING_TEAM: "Kolkata Knight Riders", "Delhi Capitals", "Sunrisers Hyderabad"
STRIKER: "Virat Kohli", "Rohit Sharma", "MS Dhoni"
BOWLER: "Jasprit Bumrah", "Rashid Khan", "Yuzvendra Chahal"
RUNS_OF_BAT: 0, 1, 2, 3, 4, 6
WICKET_TYPE: "caught", "bowled", "LBW", "run out", "stumped"
```

**Example Queries**:
```sql
-- Total matches by season
SELECT "SEASON", COUNT(DISTINCT "MATCH_ID") as total_matches 
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA" 
GROUP BY "SEASON" 
ORDER BY "SEASON";

-- Top run scorers across all seasons
SELECT "STRIKER", SUM("RUNS_OF_BAT") as total_runs, COUNT(*) as balls_faced
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "STRIKER"
ORDER BY total_runs DESC
LIMIT 20;

-- Top wicket takers across all seasons
SELECT "BOWLER", COUNT("WICKET_TYPE") as wickets
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
WHERE "WICKET_TYPE" IS NOT NULL
GROUP BY "BOWLER"
ORDER BY wickets DESC
LIMIT 20;

-- Team-wise total runs by season
SELECT "SEASON", "BATTING_TEAM", SUM("RUNS_OF_BAT") as total_runs
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "SEASON", "BATTING_TEAM"
ORDER BY "SEASON", total_runs DESC;
```

---

## Important SQL Rules

1. **ALWAYS wrap ALL identifiers in double quotes - schemas, tables, AND columns**
   - ✅ CORRECT: `SELECT "MATCH_ID" FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"`
   - ✅ CORRECT: `SELECT SUM("RUNS_OF_BAT") FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"`
   - ✅ CORRECT: `SELECT "STRIKER", "BOWLER" FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"`
   - ❌ WRONG: `SELECT * FROM SILVER.T_STG_CRICKET_LEAGUE_IPL_DATA`
   - ❌ WRONG: `SELECT MATCH_ID FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"` (column not quoted)
   - Note: Use the EXACT case as defined in the database schema (UPPERCASE)

2. **Use proper table aliases with quoted column names**
   - ✅ CORRECT: `SELECT i."MATCH_ID", i."STRIKER" FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA" i`
   - ❌ WRONG: `SELECT i.MATCH_ID FROM SILVER.T_STG_CRICKET_LEAGUE_IPL_DATA i`

3. **Use proper GROUP BY** clauses when using aggregate functions

4. **String values in WHERE** use single quotes:
   - ✅ CORRECT: `WHERE "BATTING_TEAM" = 'Mumbai Indians'`
   - ❌ WRONG: `WHERE BATTING_TEAM = 'Mumbai Indians'`

5. **Date handling**: The DATE column is stored as text, use TO_TIMESTAMP for date operations if needed

---

## Common Analysis Patterns

### Season-wise Performance
```sql
SELECT 
    "SEASON",
    COUNT(DISTINCT "MATCH_ID") as total_matches,
    SUM("RUNS_OF_BAT") as total_runs,
    COUNT("WICKET_TYPE") as total_wickets
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "SEASON"
ORDER BY "SEASON";
```

### Team Performance Analysis
```sql
SELECT 
    "SEASON",
    "BATTING_TEAM",
    COUNT(DISTINCT "MATCH_ID") as matches_played,
    SUM("RUNS_OF_BAT") as total_runs,
    COUNT("WICKET_TYPE") as wickets_lost,
    AVG("RUNS_OF_BAT") as avg_runs_per_ball
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "SEASON", "BATTING_TEAM"
ORDER BY "SEASON", total_runs DESC;
```

### Bowler Statistics
```sql
SELECT 
    "BOWLER",
    "SEASON",
    COUNT(*) as balls_bowled,
    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as runs_conceded,
    COUNT("WICKET_TYPE") as wickets,
    ROUND((SUM("RUNS_OF_BAT") + SUM("EXTRAS"))::numeric / NULLIF(COUNT("WICKET_TYPE"), 0), 2) as bowling_average
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "BOWLER", "SEASON"
HAVING COUNT("WICKET_TYPE") > 0
ORDER BY "SEASON", wickets DESC;
```

### Batsman Statistics
```sql
SELECT 
    "STRIKER",
    "SEASON",
    COUNT(*) as balls_faced,
    SUM("RUNS_OF_BAT") as total_runs,
    COUNT(CASE WHEN "RUNS_OF_BAT" = 4 THEN 1 END) as fours,
    COUNT(CASE WHEN "RUNS_OF_BAT" = 6 THEN 1 END) as sixes,
    ROUND(SUM("RUNS_OF_BAT")::numeric / NULLIF(COUNT(*), 0), 2) as strike_rate
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "STRIKER", "SEASON"
ORDER BY "SEASON", total_runs DESC;
```

### Venue Analysis
```sql
SELECT 
    "VENUE",
    "SEASON",
    COUNT(DISTINCT "MATCH_ID") as matches_played,
    SUM("RUNS_OF_BAT") as total_runs,
    ROUND(AVG("RUNS_OF_BAT"), 2) as avg_runs_per_ball
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "VENUE", "SEASON"
ORDER BY "SEASON", matches_played DESC;
```

### Dismissal Types Analysis
```sql
SELECT 
    "WICKET_TYPE",
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
WHERE "WICKET_TYPE" IS NOT NULL
GROUP BY "WICKET_TYPE"
ORDER BY count DESC;
```

### Head-to-Head Team Analysis
```sql
SELECT 
    "SEASON",
    "BATTING_TEAM",
    "BOWLING_TEAM",
    COUNT(DISTINCT "MATCH_ID") as matches,
    SUM("RUNS_OF_BAT") as batting_team_runs
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "SEASON", "BATTING_TEAM", "BOWLING_TEAM"
ORDER BY "SEASON", matches DESC;
```

### Over-wise Analysis
```sql
SELECT 
    "SEASON",
    "INNINGS",
    FLOOR("OVER") as over_number,
    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as total_runs,
    COUNT("WICKET_TYPE") as wickets
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
GROUP BY "SEASON", "INNINGS", FLOOR("OVER")
ORDER BY "SEASON", "INNINGS", over_number;
```

### Powerplay Analysis (First 6 overs)
```sql
SELECT 
    "SEASON",
    "BATTING_TEAM",
    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as powerplay_runs,
    COUNT("WICKET_TYPE") as powerplay_wickets,
    ROUND((SUM("RUNS_OF_BAT") + SUM("EXTRAS"))::numeric / NULLIF(COUNT("WICKET_TYPE"), 0), 2) as runs_per_wicket
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
WHERE "OVER" < 6
GROUP BY "SEASON", "BATTING_TEAM"
ORDER BY "SEASON", powerplay_runs DESC;
```

### Death Overs Analysis (Last 4 overs)
```sql
SELECT 
    "SEASON",
    "BATTING_TEAM",
    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as death_overs_runs,
    COUNT("WICKET_TYPE") as death_overs_wickets,
    ROUND((SUM("RUNS_OF_BAT") + SUM("EXTRAS"))::numeric / NULLIF(COUNT("WICKET_TYPE"), 0), 2) as runs_per_wicket
FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
WHERE "OVER" >= 16
GROUP BY "SEASON", "BATTING_TEAM"
ORDER BY "SEASON", death_overs_runs DESC;
```
