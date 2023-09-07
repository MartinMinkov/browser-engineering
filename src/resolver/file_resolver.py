from src.resolver.resolver import Resolver
from src.utils.url import FileURL, Scheme


class FileResolver(Resolver):
    url: FileURL

    def __init__(self, url: FileURL):
        if url.scheme != Scheme.File:
            raise ValueError("Unknown scheme {}".format(url.scheme))
        self.url = url

    def resolve(self) -> str:
        with open(self.url.path, "r") as f:
            return f.read()
