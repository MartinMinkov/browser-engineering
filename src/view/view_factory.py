from src.utils.url import URL, AbstractURL, DataURL, Scheme
from src.view.data_view import DataView
from src.view.file_view import FileView
from src.view.html_view import HTMLView
from src.view.view import View


class ViewFactory:
    @staticmethod
    def create(url: AbstractURL) -> View:
        if isinstance(url, URL):
            if url.scheme == Scheme.File:
                return FileView(url)
            elif url.scheme in {Scheme.HTTP, Scheme.HTTPS}:
                return HTMLView(url)
        elif isinstance(url, DataURL):
            return DataView(url)
        raise ValueError(f"Unsupported URL type: {type(url)}")