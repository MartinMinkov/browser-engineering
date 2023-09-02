from time import sleep
from unittest import TestCase

from src.networking.cache import BrowserCache
from src.networking.headers import Headers
from src.networking.response import Response


class TestCache(TestCase):
    def test_basic_set_get(self):
        cache = BrowserCache()
        resp = Response(200, "OK", Headers({"Content-Type": "text/plain"}), "test_data")
        cache.set("test_key", resp)
        self.assertEqual(cache.get("test_key"), resp)

    def test_eviction_on_time(self):
        cache = BrowserCache()
        resp1 = Response(
            200, "OK", Headers({"Content-Type": "text/plain"}), "test_data1"
        )
        resp2 = Response(
            404, "Not Found", Headers({"Content-Type": "text/plain"}), "test_data2"
        )

        cache.set("test_key1", resp1, max_age=1)
        cache.set("test_key2", resp2, max_age=3)

        sleep(2)

        self.assertIsNone(cache.get("test_key1"))
        self.assertEqual(cache.get("test_key2"), resp2)

    def test_eviction_due_to_capacity(self):
        cache = BrowserCache(capacity=2)
        resp1 = Response(
            200, "OK", Headers({"Content-Type": "text/plain"}), "test_data1"
        )
        resp2 = Response(
            404, "Not Found", Headers({"Content-Type": "text/plain"}), "test_data2"
        )
        resp3 = Response(
            500, "Server Error", Headers({"Content-Type": "text/plain"}), "test_data3"
        )

        cache.set("test_key1", resp1)
        cache.set("test_key2", resp2)
        cache.set("test_key3", resp3)  # This should evict test_key1

        self.assertIsNone(cache.get("test_key1"))
        self.assertEqual(cache.get("test_key2"), resp2)
        self.assertEqual(cache.get("test_key3"), resp3)

    def test_unsuccessful_response(self):
        cache = BrowserCache()
        resp = Response(
            404, "Not Found", Headers({"Content-Type": "text/plain"}), "error_data"
        )
        cache.set("error_key", resp)
        self.assertEqual(cache.get("error_key"), resp)
        self.assertFalse(resp.is_successful())

    def test_cache_size(self):
        cache = BrowserCache()
        resp1 = Response(
            200, "OK", Headers({"Content-Type": "text/plain"}), "test_data1"
        )
        resp2 = Response(
            404, "Not Found", Headers({"Content-Type": "text/plain"}), "test_data2"
        )
        self.assertEqual(cache.get_capacity(), 0)

        cache.set("test_key1", resp1)
        self.assertEqual(cache.get_capacity(), 1)

        cache.set("test_key2", resp2)
        self.assertEqual(cache.get_capacity(), 2)

        cache.get("test_key1")  # Accessing should not change the size
        self.assertEqual(cache.get_capacity(), 2)
