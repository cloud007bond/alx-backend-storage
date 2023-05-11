#!/usr/bin/env python3
"""
Module implementing a Cache class for storing and
retrieving data using Redis.
"""
from functools import wraps
import redis


def count_calls(method: callable) -> callable:
    """Decorator that counts how many times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class."""
    def __init__(self):
        """Initializer."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
