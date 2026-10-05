from __future__ import annotations

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ecogrid")


def log_event(message: str, correlation_id: str | None = None):
    if correlation_id:
        logger.info(
            "%s | correlation_id=%s",
            message,
            correlation_id
        )
    else:
        logger.info(message)
