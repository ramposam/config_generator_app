# Football Database Agent

## Database Connection Details
- **Database**: ETL_PIPELINES_DB
- **Schema**: public
- **Available Tables**: PLAYER, MATCH, LEAGUE, TEAM, COUNTRY, TEAM_ATTRIBUTES, PLAYER_ATTRIBUTES

---

## Table Schemas

### 1. public.PLAYER
**Description**: Player information and details

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| PLAYER_API_ID | bigint | YES | API identifier for player |
| PLAYER_NAME | text | YES | Name of the player |
| PLAYER_FIFA_API_ID | bigint | YES | FIFA API identifier |
| BIRTHDAY | text | YES | Player's birthday |
| HEIGHT | double precision | YES | Player height in cm |
| WEIGHT | bigint | YES | Player weight in kg |

**Sample Values**:
```
player_name: "Cristiano Ronaldo", "Lionel Messi"
nationality: "Portuguese", "Argentine"
height: 187.5, 170.0
weight: 84, 72
position: "Forward", "Midfielder"
```

**Example Queries**:
```sql
-- All players and their count
SELECT COUNT(*) as total_players FROM "public"."PLAYER";

-- Players by name
SELECT "PLAYER_NAME", COUNT(*) as player_count 
FROM "public"."PLAYER" 
GROUP BY "PLAYER_NAME";

-- Average player height
SELECT AVG("HEIGHT") as avg_height FROM "public"."PLAYER";
```

---

### 2. public.MATCH
**Description**: Football match results and details

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| COUNTRY_ID | bigint | YES | Foreign key to COUNTRY |
| LEAGUE_ID | bigint | YES | Foreign key to LEAGUE |
| SEASON | text | YES | Season year (e.g., 2019-2020) |
| STAGE | text | YES | Match stage |
| DATE | text | YES | Date of the match |
| MATCH_API_ID | bigint | YES | API identifier |
| HOME_TEAM_API_ID | bigint | YES | API ID for home team |
| AWAY_TEAM_API_ID | bigint | YES | API ID for away team |
| HOME_TEAM_GOAL | bigint | YES | Goals scored by home team |
| AWAY_TEAM_GOAL | bigint | YES | Goals scored by away team |
| HOME_PLAYER_X1 | double precision | YES | Home player X position 1 |
| HOME_PLAYER_X2 | double precision | YES | Home player X position 2 |
| HOME_PLAYER_X3 | double precision | YES | Home player X position 3 |
| HOME_PLAYER_X4 | double precision | YES | Home player X position 4 |
| HOME_PLAYER_X5 | double precision | YES | Home player X position 5 |
| HOME_PLAYER_X6 | double precision | YES | Home player X position 6 |
| HOME_PLAYER_X7 | double precision | YES | Home player X position 7 |
| HOME_PLAYER_X8 | double precision | YES | Home player X position 8 |
| HOME_PLAYER_X9 | double precision | YES | Home player X position 9 |
| HOME_PLAYER_X10 | double precision | YES | Home player X position 10 |
| HOME_PLAYER_X11 | double precision | YES | Home player X position 11 |
| AWAY_PLAYER_X1 | double precision | YES | Away player X position 1 |
| AWAY_PLAYER_X2 | double precision | YES | Away player X position 2 |
| AWAY_PLAYER_X3 | double precision | YES | Away player X position 3 |
| AWAY_PLAYER_X4 | double precision | YES | Away player X position 4 |
| AWAY_PLAYER_X5 | double precision | YES | Away player X position 5 |
| AWAY_PLAYER_X6 | double precision | YES | Away player X position 6 |
| AWAY_PLAYER_X7 | double precision | YES | Away player X position 7 |
| AWAY_PLAYER_X8 | double precision | YES | Away player X position 8 |
| AWAY_PLAYER_X9 | double precision | YES | Away player X position 9 |
| AWAY_PLAYER_X10 | double precision | YES | Away player X position 10 |
| AWAY_PLAYER_X11 | double precision | YES | Away player X position 11 |
| HOME_PLAYER_Y1 | double precision | YES | Home player Y position 1 |
| HOME_PLAYER_Y2 | double precision | YES | Home player Y position 2 |
| HOME_PLAYER_Y3 | double precision | YES | Home player Y position 3 |
| HOME_PLAYER_Y4 | double precision | YES | Home player Y position 4 |
| HOME_PLAYER_Y5 | double precision | YES | Home player Y position 5 |
| HOME_PLAYER_Y6 | double precision | YES | Home player Y position 6 |
| HOME_PLAYER_Y7 | double precision | YES | Home player Y position 7 |
| HOME_PLAYER_Y8 | double precision | YES | Home player Y position 8 |
| HOME_PLAYER_Y9 | double precision | YES | Home player Y position 9 |
| HOME_PLAYER_Y10 | double precision | YES | Home player Y position 10 |
| HOME_PLAYER_Y11 | double precision | YES | Home player Y position 11 |
| AWAY_PLAYER_Y1 | double precision | YES | Away player Y position 1 |
| AWAY_PLAYER_Y2 | double precision | YES | Away player Y position 2 |
| AWAY_PLAYER_Y3 | double precision | YES | Away player Y position 3 |
| AWAY_PLAYER_Y4 | double precision | YES | Away player Y position 4 |
| AWAY_PLAYER_Y5 | double precision | YES | Away player Y position 5 |
| AWAY_PLAYER_Y6 | double precision | YES | Away player Y position 6 |
| AWAY_PLAYER_Y7 | double precision | YES | Away player Y position 7 |
| AWAY_PLAYER_Y8 | double precision | YES | Away player Y position 8 |
| AWAY_PLAYER_Y9 | double precision | YES | Away player Y position 9 |
| AWAY_PLAYER_Y10 | double precision | YES | Away player Y position 10 |
| AWAY_PLAYER_Y11 | double precision | YES | Away player Y position 11 |
| HOME_PLAYER_1 | double precision | YES | Home player 1 |
| HOME_PLAYER_2 | double precision | YES | Home player 2 |
| HOME_PLAYER_3 | double precision | YES | Home player 3 |
| HOME_PLAYER_4 | double precision | YES | Home player 4 |
| HOME_PLAYER_5 | double precision | YES | Home player 5 |
| HOME_PLAYER_6 | double precision | YES | Home player 6 |
| HOME_PLAYER_7 | double precision | YES | Home player 7 |
| HOME_PLAYER_8 | double precision | YES | Home player 8 |
| HOME_PLAYER_9 | double precision | YES | Home player 9 |
| HOME_PLAYER_10 | double precision | YES | Home player 10 |
| HOME_PLAYER_11 | double precision | YES | Home player 11 |
| AWAY_PLAYER_1 | double precision | YES | Away player 1 |
| AWAY_PLAYER_2 | double precision | YES | Away player 2 |
| AWAY_PLAYER_3 | double precision | YES | Away player 3 |
| AWAY_PLAYER_4 | double precision | YES | Away player 4 |
| AWAY_PLAYER_5 | double precision | YES | Away player 5 |
| AWAY_PLAYER_6 | double precision | YES | Away player 6 |
| AWAY_PLAYER_7 | double precision | YES | Away player 7 |
| AWAY_PLAYER_8 | double precision | YES | Away player 8 |
| AWAY_PLAYER_9 | double precision | YES | Away player 9 |
| AWAY_PLAYER_10 | double precision | YES | Away player 10 |
| AWAY_PLAYER_11 | double precision | YES | Away player 11 |
| GOAL | text | YES | Goal information |
| SHOTON | text | YES | Shots on target |
| SHOTOFF | text | YES | Shots off target |
| FOULCOMMIT | text | YES | Fouls committed |
| CARD | text | YES | Cards given |
| CROSS | text | YES | Crosses |
| CORNER | text | YES | Corners |
| POSSESSION | text | YES | Possession percentage |
| B365H | double precision | YES | Bet365 home odds |
| B365D | double precision | YES | Bet365 draw odds |
| B365A | double precision | YES | Bet365 away odds |
| BWH | double precision | YES | BW home odds |
| BWD | double precision | YES | BW draw odds |
| BWA | double precision | YES | BW away odds |
| IWH | double precision | YES | IW home odds |
| IWD | double precision | YES | IW draw odds |
| IWA | double precision | YES | IW away odds |
| LBH | double precision | YES | LB home odds |
| LBD | double precision | YES | LB draw odds |
| LBA | double precision | YES | LB away odds |
| PSH | double precision | YES | PS home odds |
| PSD | double precision | YES | PS draw odds |
| PSA | double precision | YES | PS away odds |
| WHH | double precision | YES | WH home odds |
| WHD | double precision | YES | WH draw odds |
| WHA | double precision | YES | WH away odds |
| SJH | double precision | YES | SJ home odds |
| SJD | double precision | YES | SJ draw odds |
| SJA | double precision | YES | SJ away odds |
| VCH | double precision | YES | VC home odds |
| VCD | double precision | YES | VC draw odds |
| VCA | double precision | YES | VC away odds |
| GBH | double precision | YES | GB home odds |
| GBD | double precision | YES | GB draw odds |
| GBA | double precision | YES | GB away odds |
| BSH | double precision | YES | BS home odds |
| BSD | double precision | YES | BS draw odds |
| BSA | double precision | YES | BS away odds |

**Sample Values**:
```
home_team_goal: 1, 2, 3, 0
away_team_goal: 1, 0, 2, 1
match_date: 2023-09-15
season: 2023-2024
```

**Example Queries**:
```sql
-- Total matches
SELECT COUNT(*) as total_matches FROM "public"."MATCH";

-- Match statistics
SELECT 
    COUNT(*) as total_matches,
    SUM(CASE WHEN "HOME_TEAM_GOAL" > "AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN "HOME_TEAM_GOAL" < "AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as away_wins,
    SUM(CASE WHEN "HOME_TEAM_GOAL" = "AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as draws
FROM "public"."MATCH";

-- Highest scoring matches
SELECT * FROM "public"."MATCH" 
ORDER BY ("HOME_TEAM_GOAL" + "AWAY_TEAM_GOAL") DESC 
LIMIT 10;
```

---

### 3. public.TEAM
**Description**: Football team information

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| TEAM_API_ID | bigint | YES | API identifier |
| TEAM_FIFA_API_ID | double precision | YES | FIFA API identifier |
| TEAM_LONG_NAME | text | YES | Full team name |
| TEAM_SHORT_NAME | text | YES | Short team abbreviation |

**Sample Values**:
```
team_short_name: "MU", "LIV", "ARS"
team_long_name: "Manchester United", "Liverpool", "Arsenal"
```

**Example Queries**:
```sql
-- All teams
SELECT COUNT(*) as total_teams FROM "public"."TEAM";

-- Teams by name
SELECT * FROM "public"."TEAM" 
WHERE "TEAM_LONG_NAME" LIKE '%Manchester%';
```

---

### 4. public.LEAGUE
**Description**: Football league information

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| COUNTRY_ID | bigint | YES | Foreign key to COUNTRY |
| LEAGUE_NAME | text | YES | League name |

**Sample Values**:
```
league_name: "Premier League", "La Liga", "Serie A"
```

**Example Queries**:
```sql
-- All leagues
SELECT COUNT(*) as total_leagues FROM "public"."LEAGUE";

-- Leagues per country
SELECT "COUNTRY_ID", COUNT(*) as league_count 
FROM "public"."LEAGUE" 
GROUP BY "COUNTRY_ID";
```

---

### 5. public.COUNTRY
**Description**: Country information

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| COUNTRY_NAME | text | YES | Name of the country |

**Sample Values**:
```
country_name: "England", "Spain", "Italy", "Germany"
```

**Example Queries**:
```sql
-- All countries
SELECT COUNT(*) as total_countries FROM "public"."COUNTRY";

-- Countries with teams
SELECT c."COUNTRY_NAME", COUNT(DISTINCT l."ID") as league_count
FROM "public"."COUNTRY" c
LEFT JOIN "public"."LEAGUE" l ON c."ID" = l."COUNTRY_ID"
GROUP BY c."COUNTRY_NAME";
```

---

### 6. public.PLAYER_ATTRIBUTES
**Description**: Player performance attributes and ratings

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| PLAYER_FIFA_API_ID | bigint | YES | FIFA API identifier |
| PLAYER_API_ID | bigint | YES | API identifier for player |
| DATE | text | YES | Date of attributes |
| OVERALL_RATING | double precision | YES | Overall rating (1-100) |
| POTENTIAL | double precision | YES | Potential rating (1-100) |
| PREFERRED_FOOT | text | YES | Preferred foot (left/right) |
| ATTACKING_WORK_RATE | text | YES | Attacking work rate |
| DEFENSIVE_WORK_RATE | text | YES | Defensive work rate |
| CROSSING | double precision | YES | Crossing attribute |
| FINISHING | double precision | YES | Finishing attribute |
| HEADING_ACCURACY | double precision | YES | Heading accuracy |
| SHORT_PASSING | double precision | YES | Short passing |
| VOLLEYS | double precision | YES | Volleys attribute |
| DRIBBLING | double precision | YES | Dribbling attribute |
| CURVE | double precision | YES | Curve attribute |
| FREE_KICK_ACCURACY | double precision | YES | Free kick accuracy |
| LONG_PASSING | double precision | YES | Long passing |
| BALL_CONTROL | double precision | YES | Ball control |
| ACCELERATION | double precision | YES | Acceleration |
| SPRINT_SPEED | double precision | YES | Sprint speed |
| AGILITY | double precision | YES | Agility |
| REACTIONS | double precision | YES | Reactions |
| BALANCE | double precision | YES | Balance |
| SHOT_POWER | double precision | YES | Shot power |
| JUMPING | double precision | YES | Jumping |
| STAMINA | double precision | YES | Stamina |
| STRENGTH | double precision | YES | Strength |
| LONG_SHOTS | double precision | YES | Long shots |
| AGGRESSION | double precision | YES | Aggression |
| INTERCEPTIONS | double precision | YES | Interceptions |
| POSITIONING | double precision | YES | Positioning |
| VISION | double precision | YES | Vision |
| PENALTIES | double precision | YES | Penalties |
| MARKING | double precision | YES | Marking |
| STANDING_TACKLE | double precision | YES | Standing tackle |
| SLIDING_TACKLE | double precision | YES | Sliding tackle |
| GK_DIVING | double precision | YES | Goalkeeper diving |
| GK_HANDLING | double precision | YES | Goalkeeper handling |
| GK_KICKING | double precision | YES | Goalkeeper kicking |
| GK_POSITIONING | double precision | YES | Goalkeeper positioning |
| GK_REFLEXES | double precision | YES | Goalkeeper reflexes |

**Sample Values**:
```
overall_rating: 88, 92, 75
potential: 92, 95, 78
pace: 89, 87, 80
shooting: 93, 92, 70
```

**Example Queries**:
```sql
-- Top rated players
SELECT p."PLAYER_NAME", pa."OVERALL_RATING", pa."POTENTIAL"
FROM "public"."PLAYER" p
JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."PLAYER_API_ID" = pa."PLAYER_API_ID"
ORDER BY pa."OVERALL_RATING" DESC
LIMIT 20;

-- Average overall rating
SELECT AVG("OVERALL_RATING") as avg_rating FROM "public"."PLAYER_ATTRIBUTES";
```

---

### 7. public.TEAM_ATTRIBUTES
**Description**: Team performance attributes and ratings

| Column Name | Data Type | Nullable | Notes |
|-------------|-----------|----------|-------|
| ID | bigint | YES | Primary key |
| TEAM_FIFA_API_ID | bigint | YES | FIFA API identifier |
| TEAM_API_ID | bigint | YES | API identifier for team |
| DATE | text | YES | Date of attributes |
| BUILDUPPLAYSPEED | bigint | YES | Build-up play speed |
| BUILDUPPLAYSPEEDCLASS | text | YES | Build-up play speed class |
| BUILDUPPLAYDRIBBLING | double precision | YES | Build-up play dribbling |
| BUILDUPPLAYDRIBBLINGCLASS | text | YES | Build-up play dribbling class |
| BUILDUPPLAYPASSING | bigint | YES | Build-up play passing |
| BUILDUPPLAYPASSINGCLASS | text | YES | Build-up play passing class |
| BUILDUPPLAYPOSITIONINGCLASS | text | YES | Build-up play positioning class |
| CHANCECREATIONPASSING | bigint | YES | Chance creation passing |
| CHANCECREATIONPASSINGCLASS | text | YES | Chance creation passing class |
| CHANCECREATIONCROSSING | bigint | YES | Chance creation crossing |
| CHANCECREATIONCROSSINGCLASS | text | YES | Chance creation crossing class |
| CHANCECREATIONSHOOTING | bigint | YES | Chance creation shooting |
| CHANCECREATIONSHOOTINGCLASS | text | YES | Chance creation shooting class |
| CHANCECREATIONPOSITIONINGCLASS | text | YES | Chance creation positioning class |
| DEFENCEPRESSURE | bigint | YES | Defence pressure |
| DEFENCEPRESSURECLASS | text | YES | Defence pressure class |
| DEFENCEAGGRESSION | bigint | YES | Defence aggression |
| DEFENCEAGGRESSIONCLASS | text | YES | Defence aggression class |
| DEFENCETEAMWIDTH | bigint | YES | Defence team width |
| DEFENCETEAMWIDTHCLASS | text | YES | Defence team width class |
| DEFENCEDEFENDERLINECLASS | text | YES | Defence defender line class |

**Sample Values**:
```
buildUpPlaySpeed: 60, 65, 55
buildUpPlayPassing: "Short", "Long", "Mixed"
defenseAggression: 70, 60, 50
```

**Example Queries**:
```sql
-- Team attributes
SELECT * FROM "public"."TEAM_ATTRIBUTES" 
WHERE "TEAM_API_ID" = 1;

-- Teams with aggressive defense
SELECT t."TEAM_LONG_NAME", ta."DEFENCEAGGRESSION"
FROM "public"."TEAM" t
JOIN "public"."TEAM_ATTRIBUTES" ta ON t."TEAM_API_ID" = ta."TEAM_API_ID"
WHERE ta."DEFENCEAGGRESSION" > 75
ORDER BY ta."DEFENCEAGGRESSION" DESC;
```

---

## Important SQL Rules

1. **ALWAYS wrap table names, schema names, and database names in double quotes**
   - ✅ CORRECT: `SELECT * FROM "public"."PLAYER"`
   - ✅ CORRECT: `SELECT * FROM "ETL_PIPELINES_DB"."public"."PLAYER"`
   - ✅ CORRECT: `SELECT "OVERALL_RATING" FROM "public"."PLAYER_ATTRIBUTES"` (if column is uppercase)
   - ❌ WRONG: `SELECT * FROM public.PLAYER`
   - Note: Use the EXACT case as defined in the database schema

2. **Use proper table aliases** for complex queries with multiple tables

3. **Always include JOINs** when combining data from multiple tables

4. **Use proper GROUP BY** clauses when using aggregate functions

## Common Analysis Patterns

### Player Analysis
```sql
SELECT 
    p."ID",
    p."PLAYER_NAME",
    p."BIRTHDAY",
    p."HEIGHT",
    p."WEIGHT",
    pa."OVERALL_RATING",
    pa."POTENTIAL",
    pa."FINISHING",
    pa."DRIBBLING",
    pa."PASSING"
FROM "public"."PLAYER" p
LEFT JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."PLAYER_API_ID" = pa."PLAYER_API_ID"
WHERE pa."OVERALL_RATING" IS NOT NULL
ORDER BY pa."OVERALL_RATING" DESC;
```

### Match Statistics
```sql
SELECT 
    l."LEAGUE_NAME",
    c."COUNTRY_NAME",
    COUNT(m."ID") as total_matches,
    SUM(CASE WHEN m."HOME_TEAM_GOAL" > m."AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN m."HOME_TEAM_GOAL" < m."AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as away_wins,
    SUM(CASE WHEN m."HOME_TEAM_GOAL" = m."AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as draws,
    AVG(m."HOME_TEAM_GOAL" + m."AWAY_TEAM_GOAL") as avg_goals_per_match
FROM "public"."MATCH" m
JOIN "public"."LEAGUE" l ON m."LEAGUE_ID" = l."ID"
JOIN "public"."COUNTRY" c ON l."COUNTRY_ID" = c."ID"
GROUP BY l."LEAGUE_NAME", c."COUNTRY_NAME";
```

### Team Performance
```sql
SELECT 
    t."TEAM_LONG_NAME",
    COUNT(CASE WHEN m."HOME_TEAM_API_ID" = t."TEAM_API_ID" THEN 1 END) as home_matches,
    SUM(CASE WHEN m."HOME_TEAM_API_ID" = t."TEAM_API_ID" AND m."HOME_TEAM_GOAL" > m."AWAY_TEAM_GOAL" THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN m."AWAY_TEAM_API_ID" = t."TEAM_API_ID" AND m."AWAY_TEAM_GOAL" > m."HOME_TEAM_GOAL" THEN 1 ELSE 0 END) as away_wins,
    SUM(m."HOME_TEAM_GOAL" + m."AWAY_TEAM_GOAL") as total_goals_involved
FROM "public"."TEAM" t
LEFT JOIN "public"."MATCH" m ON (m."HOME_TEAM_API_ID" = t."TEAM_API_ID" OR m."AWAY_TEAM_API_ID" = t."TEAM_API_ID")
GROUP BY t."TEAM_LONG_NAME";
```

### Top Performers
```sql
SELECT 
    p."PLAYER_NAME",
    p."BIRTHDAY",
    pa."OVERALL_RATING",
    pa."POTENTIAL",
    pa."FINISHING",
    pa."DRIBBLING",
    pa."PASSING"
FROM "public"."PLAYER" p
JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."PLAYER_API_ID" = pa."PLAYER_API_ID"
ORDER BY pa."OVERALL_RATING" DESC
LIMIT 20;
```

