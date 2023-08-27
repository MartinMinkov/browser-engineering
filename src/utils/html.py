from src.html.html_view import HTMLView
from src.utils.url import URL


def load(url: URL):
    view = HTMLView(url)
    html_body = view.load()
    view.show(html_body)
