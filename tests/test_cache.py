from unittest import TestCase

from src.networking.cache import LRUCache


class TestCache(TestCase):
    def test_set_and_get(self):
        cache = LRUCache(size=3)

        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_over_capacity(self):
        cache = LRUCache(size=2)

        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)

        assert (
            cache.get("a") is None
        )  # "a" should be evicted as it's the least recently used
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_lru_order(self):
        cache = LRUCache(size=3)

        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache.get("a")  # Update "a" to be the most recently used
        cache.set("d", 4)  # This should evict "b" as it's now the least recently used

        assert cache.get("b") is None
        assert cache.get("a") == 1
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_update_existing_key(self):
        cache = LRUCache(size=3)

        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("a", 3)  # Update the value for key "a"

        assert cache.get("a") == 3
        assert cache.get("b") == 2

    def test_get_capacity(self):
        cache = LRUCache(size=3)

        assert cache.get_capacity() == 0  # No items added yet

        cache.set("a", 1)
        cache.set("b", 2)

        assert cache.get_capacity() == 2
