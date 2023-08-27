from src.networking.headers import Headers
from src.networking.http_client import HTTPClient
from src.networking.request import Request
from src.utils.url import URL


class HTMLView:
    def __init__(self, url: URL):
        self.url = url

    def show(self, body: str):
        in_angle = False
        for c in body:
            if c == "<":
                in_angle = True
            elif c == ">":
                in_angle = False
            elif not in_angle:
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

        encoding = "utf8"
        if (
            "content-type" in response.headers
            and "charset=" in response.headers.get_header("content-type")
        ):
            encoding = response.headers.get_header("content-type").split("charset=")[-1]

        return response.body
