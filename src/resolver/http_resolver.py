import base64

from src.networking.cache import BrowserCache
from src.networking.headers import Headers
from src.networking.http_client import HTTPClient
from src.networking.request import Request
from src.networking.response import Response
from src.resolver.resolver import Resolver
from src.utils.url import URL, Scheme


class HTTPResolver(Resolver):
    url: URL
    cache: BrowserCache

    def __init__(self, url: URL, cache: BrowserCache):
        if url.scheme not in {Scheme.HTTP, Scheme.HTTPS}:
            raise ValueError(f"Unknown scheme {url.scheme}")
        self.url = url
        self.cache = cache

    def resolve(self) -> str:
        # Check cache first
        cached_response = self.cache.get(str(self.url))
        if cached_response:
            self._validate_response(cached_response)
            return cached_response.body
        fresh_response = self._fetch_fresh_response()
        self._validate_response(fresh_response)

        # Cache the fresh response if it has a valid max_age
        self._cache_response(fresh_response, self.cache)
        return fresh_response.body

    def _validate_response(self, response: Response):
        assert (
            response.status_code == 200
        ), f"{response.status_code}: {response.reason_phrase}"
        assert "transfer-encoding" not in response.headers
        assert "content-encoding" not in response.headers

    def _fetch_fresh_response(self) -> Response:
        headers = Headers.default(self.url.host)
        request = Request(self.url, headers=headers)
        http_client = HTTPClient(self.url)
        return http_client.send_request(request)

    def _cache_response(self, response: Response, cache: BrowserCache) -> None:
        cache_control_header = response.headers.get_header("cache-control")
        if cache_control_header is None or "no-store" in cache_control_header:
            return

        if cache_control_header and "max-age=" in cache_control_header:
            max_age = int(cache_control_header.split("=")[-1])
            cache.set(str(self.url), response, max_age)
