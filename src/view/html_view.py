from src.networking.headers import Headers
from src.networking.http_client import HTTPClient
from src.networking.request import Request
from src.utils.url import URL, Scheme
from src.view.view import View


class HTMLView(View):
    def __init__(self, url: URL):
        if url.scheme != Scheme.HTTP and url.scheme != Scheme.HTTPS:
            raise ValueError("Unknown scheme {}".format(url.scheme))
        self.url = url

    def show(self, document: str):
        in_angle = False
        in_body = False
        body_tag_str = "body"
        for idx, c in enumerate(document):
            if c == "<":
                in_angle = True
                if document[idx + 1 : idx + 1 + len(body_tag_str)] == body_tag_str:
                    in_body = True
            elif c == ">":
                in_angle = False
                if (
                    document[idx - len(body_tag_str) : idx] == body_tag_str
                    and document[idx - len(body_tag_str) - 1] == "/"
                ):
                    in_body = False
            elif in_body and not in_angle:
                print(c, end="")

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
