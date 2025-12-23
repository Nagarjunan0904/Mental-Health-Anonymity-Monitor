import os
import time
import logging
import requests
from typing import Optional

class HTTPError(Exception):
    pass

DEFAULT_MAX_RETRIES = int(os.environ.get("HTTP_MAX_RETRIES", "3"))
DEFAULT_BACKOFF = float(os.environ.get("HTTP_BACKOFF", "1.5"))
DEFAULT_TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "20"))

def fetch_json(
    url: str,
    headers: dict,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff: float = DEFAULT_BACKOFF,
    timeout: int = DEFAULT_TIMEOUT
) -> dict:
    last_exc: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            if 400 <= resp.status_code < 500:
                raise HTTPError(f"HTTP {resp.status_code} for {url}")
        except Exception as e:
            last_exc = e
            logging.warning("fetch_json attempt %d failed: %s", attempt, e)
        time.sleep(backoff ** attempt)
    raise HTTPError(f"Failed after {max_retries} attempts: {url}; last={last_exc}")
