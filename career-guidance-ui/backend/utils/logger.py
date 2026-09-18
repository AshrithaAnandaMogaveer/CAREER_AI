"""
Structured request logger for Explore endpoints.
"""

import logging
import sys

# Configure root logger once
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

explore_logger = logging.getLogger("explore")


def log_request(user_id, endpoint: str, params: dict, result_summary: str, elapsed_ms: float):
    """
    Log a structured request line.
    Example: [INFO] user=12 endpoint=/explore/roi params={skill: Python} result=success time=120ms
    """
    explore_logger.info(
        f"user={user_id} endpoint={endpoint} params={params} result={result_summary} time={elapsed_ms:.0f}ms"
    )


def log_error(user_id, endpoint: str, error: str):
    explore_logger.error(f"user={user_id} endpoint={endpoint} error={error}")
