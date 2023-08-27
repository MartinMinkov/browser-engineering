from src.utils.url import URL, Scheme
from src.view.file_view import FileView
from src.view.html_view import HTMLView
from src.view.view import View


def load(url: URL):
    view: View
    if url.scheme == Scheme.File:
        view = FileView(url)
    elif url.scheme == Scheme.HTTP or url.scheme == Scheme.HTTPS:
        view = HTMLView(url)
    body = view.load()
    view.show(body)
