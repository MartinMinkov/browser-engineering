import base64
from urllib.parse import unquote

from src.resolver.resolver import Resolver
from src.utils.url import DataURL, Scheme


class DataResolver(Resolver):
    url: DataURL

    def __init__(self, url: DataURL):
        if url.scheme != Scheme.Data:
            raise ValueError("Unknown scheme {}".format(url.scheme))
        self.url = url

    def resolve(self) -> str:
        if self.url.is_base64:
            body_bytes = base64.b64decode(self.url.data)
            body_str = body_bytes.decode("utf-8")
            return unquote(body_str)
        return unquote(self.url.data)
