from enum import Enum

from src.networking.cache import BrowserCache
from src.networking.headers import Headers
from src.networking.http_client import HTTPClient
from src.networking.request import Request
from src.networking.response import Response
from src.parser.parser import Parser
from src.utils.url import URL, Scheme


class HTMLEntity(Enum):
    GreaterThan = ("&gt;", ">")
    LessThan = ("&lt;", "<")
    Amperstand = ("&amp;", "&")
    Dash = ("&dash;", "-")
    NDash = ("&ndash;", "–")
    MDash = ("&mdash;", "—")
    Copy = ("&copy;", "©")

    def conatins(self, value: str) -> bool:
        return value in self.value

    def __str__(self):
        return self.value[0]

    def symbol(self):
        return self.value[1]


class HTMLParser(Parser):
    url: URL
    inside_body_tag: bool
    in_angle_brackets: bool

    def __init__(self, url: URL):
        self.url = url
        self.inside_body_tag = False
        self.in_angle_brackets = False

        if url.scheme not in {Scheme.HTTP, Scheme.HTTPS}:
            raise ValueError(f"Unknown scheme {url.scheme}")

    def view_show(self, document: str) -> None:
        body = self.lex(document)
        print(body)

    def lex(self, document: str) -> str:
        body = self._body(document)
        return self._transform(body)

    def _body(self, document: str) -> str:
        body_document = ""
        for idx, char in enumerate(document):
            if char == "<":
                if self._is_start_of_tag(document, idx, "body"):
                    self.inside_body_tag = True
                elif self._is_start_of_tag(document, idx, "/body"):
                    self.inside_body_tag = False
                self.in_angle_brackets = True
            elif char == ">":
                self.in_angle_brackets = False
            elif self.inside_body_tag and not self.in_angle_brackets:
                body_document += char
        return body_document

    def _transform(self, document: str) -> str:
        transformed_document = ""
        idx = 0
        while idx < len(document):
            if document[idx] == "&":
                for entity in HTMLEntity:
                    if entity.conatins(document[idx : idx + len(str(entity))]):
                        transformed_document += entity.symbol()
                        idx += len(str(entity))
                        break
            transformed_document += document[idx]
            idx += 1
        return transformed_document

    def _is_start_of_tag(self, document: str, idx: int, tag: str) -> bool:
        return document[idx : idx + len(tag) + 1] == f"<{tag}"

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

    def view_load(self, cache: BrowserCache) -> str:
        # Check cache first
        cached_response = cache.get(str(self.url))
        if cached_response:
            self._validate_response(cached_response)
            return cached_response.body
        fresh_response = self._fetch_fresh_response()
        self._validate_response(fresh_response)

        # Cache the fresh response if it has a valid max_age
        self._cache_response(fresh_response, cache)
        return fresh_response.body
