"""
In-memory response cache with TTL support.
Usage: @cache_response(ttl=300)
"""

import time
import hashlib
import json
import logging
from functools import wraps

logger = logging.getLogger(__name__)

_cache = {}  # { key: (value, expires_at) }


def _make_key(user_id, endpoint, body: dict) -> str:
    body_hash = hashlib.md5(
        json.dumps(sorted(body.items()) if body else [], sort_keys=True).encode()
    ).hexdigest()[:8]
    return f"{user_id}:{endpoint}:{body_hash}"


def cache_response(ttl: int = 300):
    """Decorator — caches the JSON response tuple (dict, status_code) for `ttl` seconds."""
    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            from flask import request as flask_request
            try:
                body = flask_request.get_json(silent=True) or {}
                params = dict(flask_request.args)
                combined = {**body, **params}
                key = _make_key(current_user, flask_request.path, combined)

                # Check cache hit
                if key in _cache:
                    value, expires_at = _cache[key]
                    if time.time() < expires_at:
                        logger.debug(f"Cache HIT  key={key}")
                        return value
                    else:
                        del _cache[key]

                # Cache miss — compute
                result = f(current_user, *args, **kwargs)
                _cache[key] = (result, time.time() + ttl)
                logger.debug(f"Cache MISS key={key}")
                return result
            except Exception as e:
                logger.warning(f"Cache error ({e}), falling back to fresh compute")
                return f(current_user, *args, **kwargs)
        return wrapper
    return decorator


def invalidate_user_cache(user_id):
    """Remove all cached entries for a given user."""
    keys_to_delete = [k for k in _cache if k.startswith(f"{user_id}:")]
    for k in keys_to_delete:
        del _cache[k]
