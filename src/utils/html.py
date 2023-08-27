from src.utils.url import AbstractURL
from src.view.view_factory import ViewFactory


def load(url: AbstractURL):
    view = ViewFactory.create(url)
    body = view.load()
    view.show(body)
