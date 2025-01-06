# app/services/cache.py
import json
import redis
import logging

# Connect to Redis
# Potentially wrap in a try/except here or in the calling code
redis_client = redis.Redis(host="localhost", port=6379, db=0)

def get_cached_response(key: str):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except redis.exceptions.ConnectionError as e:
        logging.warning(f"Redis connection error on GET: {e}")
        return None  # failover: just return None
    return None

def set_cached_response(key: str, value: dict, ttl: int = 60):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except redis.exceptions.ConnectionError as e:
        logging.warning(f"Redis connection error on SET: {e}")
        # failover: do nothing, ignore cache
