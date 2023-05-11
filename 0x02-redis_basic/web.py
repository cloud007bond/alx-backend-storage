#!/usr/bin/env python3
import requests
import redis
import time

class WebCache:
    def __init__(self):
        self.redis = redis.Redis()

    def cache(self, fn):
        def wrapper(url):
            count_key = f"count:{url}"
            content_key = f"content:{url}"

            # Check if the content is already in cache
            cached_content = self.redis.get(content_key)
            if cached_content:
                return cached_content

            # Retrieve the content using the wrapped function
            content = fn(url)

            # Cache the content for 10 seconds
            self.redis.setex(content_key, 10, content)

            # Increment the count for this URL
            self.redis.incr(count_key)

            return content
        return wrapper

    @cache
    def get_page(self, url):
        response = requests.get(url)
        return response.content

