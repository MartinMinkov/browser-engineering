from enum import Enum

from src.networking.headers import Headers
from src.networking.http_client import HTTPClient
from src.networking.request import Request
from src.utils.url import URL, Scheme
from src.view.view import View


class HTMLEntity(Enum):
    GreaterThan = "&gt;"
    LessThan = "&lt;"

    def __str__(self):
        return self.name.lower()


class HTMLView(View):
    def __init__(self, url: URL):
        if url.scheme != Scheme.HTTP and url.scheme != Scheme.HTTPS:
            raise ValueError("Unknown scheme {}".format(url.scheme))
        self.url = url

    def show(self, document: str):
        if self.url.is_view_source:
            print(document)
            return

        inside_body_tag = False
        in_angle_brackets = False
        for idx, char in enumerate(document):
            if char == "<":
                if self._is_start_of_tag(document, idx, "body"):
                    inside_body_tag = True
                elif self._is_start_of_tag(document, idx, "/body"):
                    inside_body_tag = False
                in_angle_brackets = True
                continue

            if char == ">":
                in_angle_brackets = False
                continue

            if inside_body_tag and not in_angle_brackets:
                char = self._replace_html_entities(char, document, idx)
                print(char, end="")

    def _is_start_of_tag(self, document: str, idx: int, tag: str) -> bool:
        return document[idx : idx + len(tag) + 1] == f"<{tag}"

    def _replace_html_entities(self, char: str, document: str, idx: int) -> str:
        if char == "&":
            if document.startswith(HTMLEntity.GreaterThan.value, idx):
                return ">"
            elif document.startswith(HTMLEntity.LessThan.value, idx):
                return "<"
        return char

    def load(self):
        headers = Headers.default(self.url.host)
        request = Request(self.url, headers=headers)

        http_client = HTTPClient(self.url)
        response = http_client.send_request(request)

        assert response.status_code == 200, "{}: {}".format(
            response.status_code, response.reason_phrase
        )

        assert "transfer-encoding" not in response.headers
        assert "content-encoding" not in response.headers

        encoding = http_client.encoding
        if (
            "content-type" in response.headers
            and "charset=" in response.headers.get_header("content-type")
        ):
            encoding = response.headers.get_header("content-type").split("charset=")[-1]
        return response.body
