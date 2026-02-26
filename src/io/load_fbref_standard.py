import io
import re
from pathlib import Path

import pandas as pd

SEASON = "2023-2024"
HTML_PATH = Path("data/raw/fbref/2023-2024/players_standard.html")

OUT_PATH = Path(f"data/processed/fbref/standard_{SEASON}.parquet")


def _extract_table_blocks(html: str) -> list[str]:
    """
    Extract raw <table>...</table> HTML blocks from:
      1) the main HTML
      2) HTML comments <!-- ... --> (FBref pattern)
    """
    blocks: list[str] = []

    # Direct tables in the HTML
    blocks.extend(re.findall(r"(<table[\s\S]*?</table>)", html, flags=re.IGNORECASE))

    # Tables inside HTML comments
    for comment_body in re.findall(r"<!--([\s\S]*?)-->", html):
        if "<table" not in comment_body.lower():
            continue
        blocks.extend(re.findall(r"(<table[\s\S]*?</table>)", comment_body, flags=re.IGNORECASE))

    return blocks


def _parse_table_blocks(table_blocks: list[str]) -> list[pd.DataFrame]:
    """Parse each <table>...</table> block into DataFrames."""
    tables: list[pd.DataFrame] = []
    for tb in table_blocks:
        try:
            dfs = pd.read_html(io.StringIO(tb))
            tables.extend(dfs)
        except Exception:
            continue
    return tables


def _pick_standard_table(tables: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Pick the most likely 'Standard' players table.
    Heuristic:
      - must include 'Player' column
      - prefer largest row count
    """
    candidates = []
    for t in tables:
        cols = [str(c) for c in t.columns]
        if "Player" in cols:
            candidates.append(t)

    if candidates:
        return max(candidates, key=lambda d: d.shape[0])

    # Fallback: just take the biggest table
    return max(tables, key=lambda d: d.shape[0])


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten MultiIndex columns and normalize to snake_case."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(c) for c in col if c and "Unnamed" not in str(c)])
            for col in df.columns
        ]

    df.columns = (
        pd.Index(df.columns)
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace("%", "pct", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return df


def load_standard_from_local_html(path: Path, season: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path.resolve()}")

    html = path.read_text(encoding="utf-8", errors="replace")

    # DEBUG (leave on until stable)
    # print("DEBUG | bytes:", path.stat().st_size)
    # print("DEBUG | <table count:", html.lower().count("<table"))
    # print("DEBUG | comments count:", html.count("<!--"))

    table_blocks = _extract_table_blocks(html)
    if not table_blocks:
        raise ValueError(
            "No <table>...</table> blocks found. "
            "Your saved HTML likely doesn't include the table markup. "
            "Try saving from 'View Page Source' on FBref."
        )

    tables = _parse_table_blocks(table_blocks)
    if not tables:
        raise ValueError("Found <table> blocks, but none could be parsed by pandas.read_html().")

    df = _pick_standard_table(tables)

    # Drop repeated header rows inside tbody
    if "Player" in df.columns:
        df = df[df["Player"] != "Player"].reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

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

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_PATH, index=False)
    print("Saved to:", OUT_PATH)