import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = Path("db/scouting.duckdb")
PARQUET_PATH = Path("data/processed/fbref/standard_2023-2024.parquet")

TABLE_NAME = "stg_fbref_standard_2023_2024"

def main():
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(f"Parquet not found at {PARQUET_PATH}")

    df = pd.read_parquet(PARQUET_PATH)

    con = duckdb.connect(str(DB_PATH))
    con.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    con.register("df", df)
    con.execute(f"CREATE TABLE {TABLE_NAME} AS SELECT * FROM df")

    rows = con.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    print(f"Loaded {rows} rows into {TABLE_NAME}")

    con.close()

if __name__ == "__main__":
    main()
