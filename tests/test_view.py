from os import remove
from unittest import TestCase
from unittest.mock import patch

from src.utils.url import URL, DataURL, FileURL
from src.view.data_view import DataView
from src.view.file_view import FileView
from src.view.html_view import HTMLView


class TestDataView(TestCase):
    def setUp(self):
        self.data_url = DataURL("data:text/plain;charset=UTF-8,Hello,%20World!")
        self.view = DataView(self.data_url)

    def test_initialization(self):
        self.assertIsInstance(self.view, DataView)

    def test_view_show_base64(self):
        with patch("builtins.print") as mock_print:
            data_url = DataURL("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
            view = DataView(data_url)
            view.view_show(data_url.data)
            mock_print.assert_called_once_with("Hello, World!")

    def test_view_load(self):
        self.assertEqual(self.view.view_load(), "Hello,%20World!")


class TestFileView(TestCase):
    def setUp(self):
        self.file_url = FileURL("file:///tmp/testfile.txt")
        with open("/tmp/testfile.txt", "w") as f:
            f.write("Hello World!")
        self.view = FileView(self.file_url)

    def tearDown(self):
        # Cleanup after test
        try:
            remove("/tmp/testfile.txt")
        except:
            pass

    def test_initialization(self):
        self.assertIsInstance(self.view, FileView)

    def test_view_load(self):
        self.assertEqual(self.view.view_load(), "Hello World!")


class TestHTMLView(TestCase):
    def setUp(self):
        self.html_url = URL("http://example.com")
        self.view = HTMLView(self.html_url)

    def test_initialization(self):
        self.assertIsInstance(self.view, HTMLView)

    def test_body_extraction(self):
        document = "<html><head></head><body>Hello, World!</body></html>"
        self.assertEqual(self.view._body(document), "Hello, World!")
