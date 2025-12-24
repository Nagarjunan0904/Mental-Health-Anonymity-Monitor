import os
import sqlite3
import pandas as pd

DB_PATH = "../data/data.db"

def main():
    con = sqlite3.connect(DB_PATH)

    query = """
    SELECT
      id,
      source,
      board_or_sub,
      created_utc,
      text
    FROM posts
    WHERE
      (source = '4chan' AND board_or_sub IN ('adv', 'r9k'))
      OR
      (source = 'reddit' AND board_or_sub IN ('depression', 'offmychest', 'Anxiety'));
    """

    df = pd.read_sql_query(query, con)
    con.close()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/mham_posts.csv", index=False)
    print("Exported", len(df), "posts to analysis/data/mham_posts.csv")

if __name__ == "__main__":
    main()
