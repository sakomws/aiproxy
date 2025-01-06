# app/services/rate_limiting.py

import time
from fastapi import HTTPException, status
from app.config import Config

# In-memory store for request timestamps
request_timestamps = []

def check_rate_limit() -> None:
    """
    Naive in-memory rate limit check.
    Removes outdated timestamps, then compares count against limit.
    """
    current_time = time.time()
    # Remove timestamps older than the RATE_LIMIT_WINDOW
    while request_timestamps and (current_time - request_timestamps[0] > Config.RATE_LIMIT_WINDOW):
        request_timestamps.pop(0)

    if len(request_timestamps) >= Config.RATE_LIMIT_COUNT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )
    
    request_timestamps.append(current_time)