import os
import time
import logging
from db import connect, init_db
from crawler_4chan import crawl_4chan_cycle
from crawler_reddit import crawl_reddit_cycle

def load_env_file(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

def _split_csv(val):
    return [x.strip() for x in val.split(",") if x.strip()]

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    setup_logging()
    load_env_file(".env")

    db_path = os.getenv("DB_PATH", "data/data.db")
    poll_4chan = int(os.getenv("POLL_SECONDS_4CHAN", 30))
    poll_reddit = int(os.getenv("POLL_SECONDS_REDDIT", 45))
    boards = _split_csv(os.getenv("BOARDS", "adv,r9k"))
    subs = _split_csv(os.getenv("SUBREDDITS", "depression,mentalhealth,Anxiety"))
    fourchan_base = os.getenv("FOURCHAN_BASE", "https://a.4cdn.org")
    reddit_base = os.getenv("REDDIT_BASE", "https://www.reddit.com")
    user_agent = os.getenv("USER_AGENT", "SMDP-Project1-Collector/0.1")

    con = connect(db_path)
    init_db(con)
    logging.info("Starting collectors — 4chan=%s, reddit=%s", boards, subs)

    last_4chan = last_reddit = 0.0
    while True:
        now = time.time()
        try:
            if now - last_4chan >= poll_4chan:
                n = crawl_4chan_cycle(con, fourchan_base, boards, user_agent)
                logging.info("4chan: inserted %d posts", n)
                last_4chan = now
        except Exception as e:
            logging.exception("4chan failed: %s", e)
        try:
            if now - last_reddit >= poll_reddit:
                n = crawl_reddit_cycle(con, reddit_base, subs, user_agent)
                logging.info("reddit: inserted %d posts", n)
                last_reddit = now
        except Exception as e:
            logging.exception("reddit failed: %s", e)
        time.sleep(2)

if __name__ == "__main__":
    main()
