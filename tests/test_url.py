from unittest import TestCase

from src.utils.url import URL, DataURL, FileURL, Scheme


class TestScheme(TestCase):
    def test_scheme(self):
        assert str(Scheme.HTTP) == "http"
        assert str(Scheme.HTTPS) == "https"
        assert str(Scheme.File) == "file"
        assert str(Scheme.Data) == "data"
        assert str(Scheme.ViewSource) == "view-source"


class TestURL(TestCase):
    def test_url(self):
        url = URL("http://example.com/test")
        assert url.scheme == Scheme.HTTP
        assert url.host == "example.com"
        assert url.path == "/test"
        assert url.port == 80

        url_with_port = URL("https://example.com:8080/test")
        assert url_with_port.scheme == Scheme.HTTPS
        assert url_with_port.host == "example.com"
        assert url_with_port.path == "/test"
        assert url_with_port.port == 8080


class TestDataURL(TestCase):
    def test_data_url(self):
        data_url = DataURL("data:text/plain;charset=UTF-8,Hello,%20World!")
        assert data_url.scheme == Scheme.Data
        assert data_url.media_type == "text/plain;charset=UTF-8"
        assert data_url.is_base64 == False
        assert data_url.data == "Hello,%20World!"


class TestFileURL(TestCase):
    def test_file_url(self):
        file_url = FileURL("file:///home/user/test.txt")
        assert file_url.scheme == Scheme.File
        assert file_url.path == "/home/user/test.txt"
