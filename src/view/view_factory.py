from src.utils.url import URL, AbstractURL, DataURL, FileURL
from src.view.data_view import DataView
from src.view.file_view import FileView
from src.view.html_view import HTMLView
from src.view.view import View


class ViewFactory:
    @staticmethod
    def create(url: AbstractURL) -> View:
        if isinstance(url, URL):
            return HTMLView(url)
        elif isinstance(url, FileURL):
            return FileView(url)
        elif isinstance(url, DataURL):
            return DataView(url)
        raise ValueError(f"Unsupported URL type: {type(url)}")
