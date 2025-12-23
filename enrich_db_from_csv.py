

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "data", "data.db")
CSV_PATH = os.path.join(BASE_DIR, "analysis", "data", "mham_annotated_sample.csv")

def add_columns_if_missing(con: sqlite3.Connection) -> None:
    """
    Add analysis columns to posts if they do not exist.
    SQLite doesn't support IF NOT EXISTS on ADD COLUMN,
    so we catch the 'duplicate column' error.
    """
    cols = [
        "ALTER TABLE posts ADD COLUMN toxicity REAL",
        "ALTER TABLE posts ADD COLUMN insult REAL",
        "ALTER TABLE posts ADD COLUMN identity_attack REAL",
        "ALTER TABLE posts ADD COLUMN is_toxic INTEGER",
        "ALTER TABLE posts ADD COLUMN sentiment_polarity REAL",
        "ALTER TABLE posts ADD COLUMN sentiment_subjectivity REAL",
    ]

    cur = con.cursor()
    for stmt in cols:
        try:
            cur.execute(stmt)
        except sqlite3.OperationalError as e:
            # Column already exists -> ignore
            if "duplicate column name" not in str(e):
                raise
    con.commit()

def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"DB not found at {DB_PATH}")
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"CSV not found at {CSV_PATH}")

    print(f"Loading annotated CSV from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    
    needed_cols = [
        "id",
        "toxicity",
        "insult",
        "identity_attack",
        "is_toxic",
        "sentiment_polarity",
        "sentiment_subjectivity",
    ]
    for col in needed_cols:
        if col not in df.columns:
            raise SystemExit(f"Column {col!r} missing from CSV")

    df = df[needed_cols].copy()

   
    con = sqlite3.connect(DB_PATH)
    add_columns_if_missing(con)

    print("Updating posts table with sentiment + toxicity values...")
    update_sql = """
        UPDATE posts
        SET
          toxicity = ?,
          insult = ?,
          identity_attack = ?,
          is_toxic = ?,
          sentiment_polarity = ?,
          sentiment_subjectivity = ?
        WHERE id = ?
    """

    rows = []
    for _, row in df.iterrows():
        rows.append((
            None if pd.isna(row["toxicity"]) else float(row["toxicity"]),
            None if pd.isna(row["insult"]) else float(row["insult"]),
            None if pd.isna(row["identity_attack"]) else float(row["identity_attack"]),
            None if pd.isna(row["is_toxic"]) else int(row["is_toxic"]),
            None if pd.isna(row["sentiment_polarity"]) else float(row["sentiment_polarity"]),
            None if pd.isna(row["sentiment_subjectivity"]) else float(row["sentiment_subjectivity"]),
            int(row["id"]),
        ))

    cur = con.cursor()
    cur.executemany(update_sql, rows)
    con.commit()
    con.close()
    print(f"Updated {len(rows)} rows in posts")

if __name__ == "__main__":
    main()
