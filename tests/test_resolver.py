from unittest import TestCase
from unittest.mock import Mock, patch

import pytest

from src.resolver.data_resolver import DataResolver
from src.resolver.file_resolver import FileResolver
from src.resolver.http_resolver import HTTPResolver
from src.utils.url import URL, DataURL, FileURL, Scheme


class TestDataResolver(TestCase):
    def test_data_resolver_init_wrong_scheme(self):
        with pytest.raises(ValueError):
            DataResolver(DataURL("http://example.com"))

    def test_data_resolver_resolve_base64(self):
        data_url = DataURL(
            "data:text/plain;base64,U29tZSBzYW1wbGUgdGV4dA=="
        )  # "Some sample text"
        resolver = DataResolver(data_url)
        assert resolver.resolve() == "Some sample text"

    def test_data_resolver_resolve_plain(self):
        data_url = DataURL("data:text/plain,Some%20sample%20text")
        resolver = DataResolver(data_url)
        assert resolver.resolve() == "Some sample text"
