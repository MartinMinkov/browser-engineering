from src.networking.cache import BrowserCache
from src.resolver.data_resolver import DataResolver
from src.resolver.file_resolver import FileResolver
from src.resolver.http_resolver import HTTPResolver
from src.resolver.resolver import Resolver
from src.utils.url import URL, AbstractURL, DataURL, FileURL


class ResolverFactory:
    @staticmethod
    def create(url: AbstractURL, cache: BrowserCache) -> Resolver:
        if isinstance(url, URL):
            return HTTPResolver(url, cache)
        elif isinstance(url, FileURL):
            return FileResolver(url)
        elif isinstance(url, DataURL):
            return DataResolver(url)
        raise ValueError(f"Unsupported URL type: {type(url)}")
