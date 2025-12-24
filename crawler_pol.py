# crawler_pol.py
import requests, sqlite3, time, datetime, logging

DB_PATH = "mhams_pol_activity.db"
BOARD = "pol"
CATALOG_URL = f"https://a.4cdn.org/{BOARD}/catalog.json"
THREAD_URL = f"https://a.4cdn.org/{BOARD}/thread/{{}}.json"

logging.basicConfig(
    filename="pol_activity.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pol_activity (
            board TEXT,
            thread_id INTEGER,
            post_id INTEGER,
            created_at DATETIME,
            is_thread INTEGER
        )
    """)
    conn.commit()
    return conn

def collect(conn):
    cur = conn.cursor()
    try:
        catalog = requests.get(CATALOG_URL, timeout=10).json()
        for page in catalog:
            for thread in page["threads"]:
                tid = thread["no"]
                created = datetime.datetime.utcfromtimestamp(thread["time"])
                cur.execute("INSERT INTO pol_activity VALUES (?, ?, ?, ?, ?)",
                            (BOARD, tid, tid, created, 1))
                thread_data = requests.get(THREAD_URL.format(tid), timeout=10).json()
                for post in thread_data.get("posts", []):
                    pid = post["no"]
                    created = datetime.datetime.utcfromtimestamp(post["time"])
                    cur.execute("INSERT INTO pol_activity VALUES (?, ?, ?, ?, ?)",
                                (BOARD, tid, pid, created, 0))
        conn.commit()
        logging.info("Cycle completed successfully.")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    conn = init_db()
    while True:
        collect(conn)
        time.sleep(3600)  # run hourly
