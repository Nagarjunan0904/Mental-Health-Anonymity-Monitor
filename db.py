import sqlite3
from contextlib import closing
from typing import Any, Dict, Optional

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,                -- '4chan' | 'reddit'
  board_or_sub TEXT NOT NULL,
  thread_id TEXT,
  post_id TEXT NOT NULL,
  parent_id TEXT,
  author TEXT,
  created_utc INTEGER,
  text TEXT,
  url TEXT,
  inserted_at TEXT DEFAULT (datetime('now')),
  UNIQUE(source, post_id)
);

CREATE TABLE IF NOT EXISTS cursors (
  source TEXT NOT NULL,                -- 'reddit' | '4chan'
  key TEXT NOT NULL,
  value TEXT,
  PRIMARY KEY (source, key)
);

CREATE INDEX IF NOT EXISTS idx_posts_time  ON posts(source, created_utc);
CREATE INDEX IF NOT EXISTS idx_posts_board ON posts(source, board_or_sub);
"""

def connect(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path, timeout=30, isolation_level=None)
    con.execute("PRAGMA foreign_keys=ON;")
    return con

def init_db(con: sqlite3.Connection) -> None:
    with closing(con.cursor()) as cur:
        cur.executescript(SCHEMA_SQL)

def upsert_post(con: sqlite3.Connection, row: Dict[str, Any]) -> bool:
    sql = (
        "INSERT OR IGNORE INTO posts "
        "(source, board_or_sub, thread_id, post_id, parent_id, author, created_utc, text, url) "
        "VALUES (:source, :board_or_sub, :thread_id, :post_id, :parent_id, :author, :created_utc, :text, :url)"
    )
    with closing(con.cursor()) as cur:
        cur.execute(sql, row)
        return cur.rowcount == 1

def get_cursor(con: sqlite3.Connection, source: str, key: str) -> Optional[str]:
    with closing(con.cursor()) as cur:
        cur.execute("SELECT value FROM cursors WHERE source=? AND key=?", (source, key))
        r = cur.fetchone()
        return r[0] if r else None

def set_cursor(con: sqlite3.Connection, source: str, key: str, value: str) -> None:
    with closing(con.cursor()) as cur:
        cur.execute(
            "INSERT INTO cursors(source, key, value) VALUES(?,?,?) "
            "ON CONFLICT(source, key) DO UPDATE SET value=excluded.value",
            (source, key, value),
        )
