import duckdb
import os

DB_PATH = "db/scouting.duckdb"
RAW_PATH = "data/raw/transfermarkt"

os.makedirs("db", exist_ok=True)

con = duckdb.connect(DB_PATH)

# ======================
# Dimension Tables
# ======================

con.execute(f"""
CREATE OR REPLACE TABLE dim_player AS
SELECT
    player_id,
    name AS player_name,
    date_of_birth,
    country_of_citizenship AS nationality,
    position,
    sub_position,
    foot,
    height_in_cm,
    current_club_id,
    current_club_name,
    current_club_domestic_competition_id,
    market_value_in_eur,
    highest_market_value_in_eur,
    contract_expiration_date,
    agent_name,
    url
FROM read_csv_auto('{RAW_PATH}/players.csv');
""")

con.execute(f"""
CREATE OR REPLACE TABLE dim_club AS
SELECT
    club_id,
    name AS club_name,
    domestic_competition_id
FROM read_csv_auto('{RAW_PATH}/clubs.csv');
""")

con.execute(f"""
CREATE OR REPLACE TABLE dim_competition AS
SELECT
    competition_id,
    name AS competition_name,
    country_name
FROM read_csv_auto('{RAW_PATH}/competitions.csv');
""")

# ======================
# Market Value
# ======================

con.execute(f"""
CREATE OR REPLACE TABLE fact_player_market_value AS
SELECT
    player_id,
    date,
    market_value_in_eur
FROM read_csv_auto('{RAW_PATH}/player_valuations.csv');
""")

# ======================
# Appearances
# ======================

con.execute(f"""
CREATE OR REPLACE TABLE fact_appearances AS
SELECT
    appearance_id,
    game_id,
    player_id,
    player_club_id,
    player_current_club_id,
    CAST(date AS DATE) AS match_date,
    competition_id,
    yellow_cards,
    red_cards,
    goals,
    assists,
    minutes_played,
    -- season label assuming European season starts in July
    CASE
        WHEN EXTRACT('month' FROM CAST(date AS DATE)) >= 7
            THEN CAST(EXTRACT('year' FROM CAST(date AS DATE)) AS VARCHAR) || '-' ||
                 CAST(EXTRACT('year' FROM CAST(date AS DATE)) + 1 AS VARCHAR)
        ELSE
            CAST(EXTRACT('year' FROM CAST(date AS DATE)) - 1 AS VARCHAR) || '-' ||
            CAST(EXTRACT('year' FROM CAST(date AS DATE)) AS VARCHAR)
    END AS season
FROM read_csv_auto('{RAW_PATH}/appearances.csv');
""")

con.execute("""
CREATE OR REPLACE TABLE fact_player_season_availability AS
SELECT
    player_id,
    competition_id,
    season,
    COUNT(DISTINCT game_id) AS games_played,
    SUM(minutes_played) AS season_minutes,
    AVG(minutes_played) AS minutes_per_game,
    STDDEV_POP(minutes_played) AS minutes_volatility
FROM fact_appearances
GROUP BY player_id, competition_id, season;
""")

con.execute("""
CREATE OR REPLACE TABLE scouting_universe_base AS
WITH base AS (
    SELECT
        a.player_id,
        a.competition_id,
        a.season,
        a.games_played,
        a.season_minutes,
        a.minutes_per_game,
        a.minutes_volatility,
        p.player_name,
        p.date_of_birth,
        p.nationality,
        p.position,
        p.sub_position,
        p.foot,
        p.height_in_cm,
        c.competition_name,
        c.country_name
    FROM fact_player_season_availability a
    JOIN dim_player p USING (player_id)
    JOIN dim_competition c USING (competition_id)
),
enriched AS (
    SELECT
        *,
        -- approximate age at mid-season (Jan 1 of second year)
        DATE_DIFF(
            'year',
            date_of_birth,
            CAST(SUBSTR(season, 6, 4) || '-01-01' AS DATE)
        ) AS age
    FROM base
)
SELECT *
FROM enriched
WHERE
    season_minutes >= 900
    AND age BETWEEN 18 AND 25
    AND (
        LOWER(position) LIKE '%midfield%'
        OR LOWER(position) LIKE '%wing%'
        OR LOWER(sub_position) LIKE '%wing%'
        OR LOWER(sub_position) LIKE '%attacking%'
    );
""")

# ======================
# Sanity checks
# ======================

print("Players:", con.execute("SELECT COUNT(*) FROM dim_player").fetchone())
print("Clubs:", con.execute("SELECT COUNT(*) FROM dim_club").fetchone())
print("Competitions:", con.execute("SELECT COUNT(*) FROM dim_competition").fetchone())
print("Appearances:", con.execute("SELECT COUNT(*) FROM fact_appearances").fetchone())
print("Universe base:", con.execute("SELECT COUNT(*) FROM scouting_universe_base").fetchone())
print("Universe seasons:", con.execute("SELECT season, COUNT(*) n FROM scouting_universe_base GROUP BY season ORDER BY season DESC LIMIT 8").fetchall())

con.close()

print("DuckDB build completed successfully.")