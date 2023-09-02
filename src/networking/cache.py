from typing import Any, Dict, List


class LRUCache:
    hash: Dict[str, Any]
    values: List[str]
    capacity: int

    def __init__(self, size: int = 10):
        self.hash = {}
        self.values = []
        self.capacity = size

    def set(self, key: str, value: Any) -> None:
        if key in self.hash:
            self.values.remove(key)
            self.hash[key] = value
        else:
            if len(self.values) >= self.capacity:
                lru_key = self.values.pop(0)
                del self.hash[lru_key]
            self.hash[key] = value
        self.values.append(key)

    def get(self, key: str) -> Any:
        if key in self.hash:
            self.values.remove(key)
            self.values.append(key)
            return self.hash[key]
        return None

    def get_capacity(self) -> int:
        return len(self.hash)
