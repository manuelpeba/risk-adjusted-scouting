import re
from io import StringIO
from pathlib import Path

import pandas as pd

SEASON = "2023-2024"
HTML_PATH = Path(f"data/raw/fbref/{SEASON}/players_standard.html")


def extract_tables_from_html(html: str) -> list[pd.DataFrame]:
    """Extract all HTML tables from full page HTML, including tables hidden inside <!-- comments -->."""
    tables: list[pd.DataFrame] = []

    # 1) Direct tables from full HTML (StringIO prevents pandas treating HTML as a filepath)
    try:
        tables.extend(pd.read_html(StringIO(html)))
    except Exception:
        pass

    # 2) Tables hidden inside HTML comments (FBref / Sports-Reference pattern)
    commented_blocks = re.findall(r"<!--(.*?)-->", html, flags=re.S)
    for block in commented_blocks:
        if "<table" not in block:
            continue
        try:
            tables.extend(pd.read_html(StringIO(block)))
        except Exception:
            continue

    return tables


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten FBref MultiIndex columns and normalize to snake_case."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(c) for c in col if c and "Unnamed" not in str(c)])
            for col in df.columns
        ]

    df.columns = (
        pd.Index(df.columns)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("%", "pct", regex=False)
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return df


def load_standard_from_local_html(path: Path, season: str) -> pd.DataFrame:
    """Load FBref 'Standard' players table from a locally saved HTML file."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path.resolve()}")

    html = path.read_text(encoding="utf-8", errors="ignore")
    tables = extract_tables_from_html(html)

    if not tables:
        raise ValueError("No tables found in HTML (direct or inside comments).")

    # Pick the first table that contains a 'Player' column (Standard table should)
    df = None
    for t in tables:
        if "Player" in [str(c) for c in t.columns]:
            df = t
            break
    if df is None:
        df = tables[0]

    # Remove repeated header rows that appear inside tbody
    if "Player" in df.columns:
        df = df[df["Player"] != "Player"].reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

    # Clean columns and add season
    df = clean_columns(df)
    df["season"] = season

    # Drop useless column artefacts (often constant "Matches")
    if "matches" in df.columns and df["matches"].nunique(dropna=False) == 1:
        df = df.drop(columns=["matches"])

    # Basic typing (safe coercion)
    num_cols = [
        "age",
        "born",
        "playing_time_mp",
        "playing_time_starts",
        "playing_time_min",
        "playing_time_90s",
        "performance_gls",
        "performance_ast",
        "performance_ga",
        "performance_gpk",
        "performance_pk",
        "performance_pkatt",
        "performance_crdy",
        "performance_crdr",
        "per_90_minutes_gls",
        "per_90_minutes_ast",
        "per_90_minutes_ga",
        "per_90_minutes_gpk",
        "per_90_minutes_gapk",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


if __name__ == "__main__":
    df = load_standard_from_local_html(HTML_PATH, SEASON)

    print("Loaded from:", HTML_PATH)
    print("Shape:", df.shape)
    print("Columns (first 20):", df.columns.tolist()[:20])
    print(df.head(5))

    # Persist processed output
    out_path = Path(f"data/processed/fbref/standard_{SEASON}.parquet")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    print("Saved to:", out_path)