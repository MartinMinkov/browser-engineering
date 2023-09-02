import time
from typing import Dict, List, Optional, TypedDict

from src.networking.response import Response


class CacheValue(TypedDict):
    value: Response
    max_age: int


class BrowserCache:
    cache: Dict[str, CacheValue]
    ordered_values: List[str]
    capacity: int

    def __init__(self, capacity: int = 100):
        self.cache = {}
        self.ordered_values = []
        self.capacity = capacity

    def get(self, key: str) -> Optional[Response]:
        cache_value = self.cache.get(key)
        if cache_value and cache_value["max_age"] > time.time():
            self.ordered_values.remove(key)
            self.ordered_values.append(key)
            return cache_value["value"]
        elif cache_value:
            self.ordered_values.remove(key)
            del self.cache[key]
        return None

    def set(self, key: str, value: Response, max_age: int = 60):
        if key in self.cache:
            self.ordered_values.remove(key)
        elif self.get_capacity() >= self.capacity:
            self.evict()
        self.ordered_values.append(key)
        self.cache[key] = {"value": value, "max_age": int(time.time()) + max_age}

    def evict(self):
        current_time = time.time()
        self.cache = {
            key: value
            for key, value in self.cache.items()
            if value["max_age"] > current_time
        }
        self.ordered_values = [key for key in self.ordered_values if key in self.cache]
        if self.get_capacity() >= self.capacity:
            key = self.ordered_values.pop(0)
            del self.cache[key]

    def get_capacity(self) -> int:
        return len(self.cache)
