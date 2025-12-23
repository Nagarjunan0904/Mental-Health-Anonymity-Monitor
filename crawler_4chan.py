import os
import logging
from typing import Iterable, List
from util import fetch_json
from db import upsert_post

# read configurable bases from .env or fallback defaults
FOURCHAN_CATALOG = "{base}/{board}/catalog.json"
FOURCHAN_THREAD  = "{base}/{board}/thread/{tid}.json"
BOARD_BASE = os.environ.get("FOURCHAN_BOARD_BASE", "https://boards.4channel.org")


def crawl_4chan_cycle(con, base: str, boards: Iterable[str], user_agent: str) -> int:
    """
    One polling cycle for all configured 4chan boards.
    Returns the number of new posts inserted.
    """
    headers = {"User-Agent": user_agent}
    inserted = 0

    for board in boards:
        # 1) fetch the board catalog
        catalog_url = FOURCHAN_CATALOG.format(base=base, board=board)
        try:
            data = fetch_json(catalog_url, headers=headers)
        except Exception as e:
            logging.warning("4chan catalog fetch failed for %s: %s", board, e)
            continue

        thread_ids: List[int] = []
        for page in data:  # each catalog page
            for thread in page.get("threads", []):
                tid = thread.get("no")
                if isinstance(tid, int):
                    thread_ids.append(tid)

        # 2) fetch each thread and store posts
        for tid in thread_ids:
            t_url = FOURCHAN_THREAD.format(base=base, board=board, tid=tid)
            try:
                t_data = fetch_json(t_url, headers=headers)
            except Exception as e:
                logging.warning("4chan thread fetch failed for %s/%s: %s", board, tid, e)
                continue

            for post in t_data.get("posts", []):
                row = {
                    "source": "4chan",
                    "board_or_sub": board,
                    "thread_id": str(tid),
                    "post_id": str(post.get("no")),
                    "parent_id": str(post.get("resto")) if post.get("resto") else None,
                    "author": post.get("name"),
                    "created_utc": int(post.get("time")) if post.get("time") else None,
                    "text": post.get("com") or post.get("sub"),
                    # Use configurable board URL base from .env
                    "url": f"{BOARD_BASE}/{board}/thread/{tid}#p{post.get('no')}",
                }
                if upsert_post(con, row):
                    inserted += 1

    return inserted
