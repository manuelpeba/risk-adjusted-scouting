# Data Architecture – DuckDB Schema

---

## 1. Dimension Tables

### dim_player

| Column | Type | Description |
|--------|------|------------|
| player_id | VARCHAR | Unique internal identifier |
| player_name | VARCHAR | Full name |
| date_of_birth | DATE | Date of birth |
| nationality | VARCHAR | Primary nationality |
| primary_position | VARCHAR | Position category (Winger / AM) |
| height_cm | INTEGER | Height (if available) |

---

### dim_competition

| Column | Type | Description |
|--------|------|------------|
| competition_id | VARCHAR | Unique competition ID |
| league_name | VARCHAR | League name |
| country | VARCHAR | Country |
| season | VARCHAR | Season identifier |
| league_tier | INTEGER | Tier classification |

---

### dim_club

| Column | Type | Description |
|--------|------|------------|
| club_id | VARCHAR | Unique club ID |
| club_name | VARCHAR | Club name |
| competition_id | VARCHAR | League reference |
| season | VARCHAR | Season |

---

## 2. Fact Tables

### fact_player_season_performance

| Column | Type |
|--------|------|
| player_id | VARCHAR |
| competition_id | VARCHAR |
| season | VARCHAR |
| minutes | INTEGER |
| xg_p90 | DOUBLE |
| xa_p90 | DOUBLE |
| sca_p90 | DOUBLE |
| progressive_carries_p90 | DOUBLE |
| progressive_passes_p90 | DOUBLE |
| touches_box_p90 | DOUBLE |
| take_on_success_rate | DOUBLE |

---

### fact_player_market_value

| Column | Type |
|--------|------|
| player_id | VARCHAR |
| season | VARCHAR |
| market_value_eur | DOUBLE |

---

### fact_player_availability

| Column | Type |
|--------|------|
| player_id | VARCHAR |
| season | VARCHAR |
| season_minutes | INTEGER |
| minutes_volatility | DOUBLE |
| match_density_proxy | DOUBLE |

---

## 3. Derived Table

### scouting_universe

Final modelling table created after filtering:

- Age 18–25  
- Minutes ≥ 900  
- Selected leagues  

Includes:

- All performance metrics  
- Standardised Z metrics  
- Talent score  
- Development score  
- Risk score  
- Final composite score  
- Value efficiency score