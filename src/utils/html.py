from src.networking.cache import BrowserCache
from src.utils.url import AbstractURL
from src.view.view_factory import ViewFactory


def load(url: AbstractURL, cache: BrowserCache) -> None:
    view = ViewFactory.create(url)
    body = view.view_load(cache)
    view.view_show(body)
