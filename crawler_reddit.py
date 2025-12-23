import os
import logging
from typing import Iterable
from util import fetch_json
from db import upsert_post, get_cursor, set_cursor

# read Reddit post limit from .env
REDDIT_LIMIT = int(os.environ.get("REDDIT_LIMIT", "100"))


def _new_url(base: str, sub: str, after: str | None) -> str:
    after_q = f"&after={after}" if after else ""
    return f"{base}/r/{sub}/new.json?limit={REDDIT_LIMIT}{after_q}"


def crawl_reddit_cycle(con, base: str, subs: Iterable[str], user_agent: str) -> int:
    """
    One polling cycle for all configured subreddits.
    Returns number of new posts inserted.
    """
    headers = {"User-Agent": user_agent}
    inserted = 0

    for sub in subs:
        cursor_key = f"after:{sub}"
        after = get_cursor(con, "reddit", cursor_key)
        url = _new_url(base, sub, after)

        try:
            data = fetch_json(url, headers=headers)
        except Exception as e:
            logging.warning("Reddit fetch failed for %s: %s", sub, e)
            continue

        listing = data.get("data", {})
        for child in listing.get("children", []):
            d = child.get("data", {})
            name = d.get("name")  
            post_id = d.get("id")
            thread_id = d.get("link_id") or name
            created_utc = int(d.get("created_utc")) if d.get("created_utc") else None
            author = d.get("author")
            title = d.get("title")
            selftext = d.get("selftext")
            permalink = d.get("permalink")

            text = (title or "") + ("\n\n" + selftext if selftext else "")
            row = {
                "source": "reddit",
                "board_or_sub": sub,
                "thread_id": str(thread_id) if thread_id else None,
                "post_id": str(name) if name else str(post_id),
                "parent_id": d.get("parent_id"),
                "author": author,
                "created_utc": created_utc,
                "text": text.strip() if text else None,
                "url": f"{base}{permalink}" if permalink else None,

            }
            if upsert_post(con, row):
                inserted += 1

        # advance cursor for next pagination
        new_after = listing.get("after")
        if new_after:
            set_cursor(con, "reddit", cursor_key, new_after)

    return inserted
