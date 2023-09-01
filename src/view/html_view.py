from enum import Enum

from src.networking.headers import Headers
from src.networking.http_client import HTTPClient
from src.networking.request import Request
from src.utils.url import URL, Scheme
from src.view.view import View


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


class HTMLView(View):
    url: URL
    inside_body_tag: bool
    in_angle_brackets: bool

    def __init__(self, url: URL):
        self.url = url
        self.inside_body_tag = False
        self.in_angle_brackets = False

        if url.scheme not in {Scheme.HTTP, Scheme.HTTPS}:
            raise ValueError(f"Unknown scheme {url.scheme}")

    def show(self, document: str) -> None:
        body = self._body(document)
        transformed = self._transform(body)
        print(transformed)

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

    def load(self) -> str:
        headers = Headers.default(self.url.host)
        request = Request(self.url, headers=headers)
        http_client = HTTPClient(self.url)
        response = http_client.send_request(request)

        assert (
            response.status_code == 200
        ), f"{response.status_code}: {response.reason_phrase}"
        assert "transfer-encoding" not in response.headers
        assert "content-encoding" not in response.headers

        # TODO: Do we need `encoding`?
        encoding = http_client.encoding
        if (
            "content-type" in response.headers
            and "charset=" in response.headers.get_header("content-type")
        ):
            encoding = response.headers.get_header("content-type").split("charset=")[-1]

        return response.body
