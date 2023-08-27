from src.utils.headers import Headers
from src.utils.http_client import HTTPClient
from src.utils.request import Request
from src.utils.response import Response
from src.utils.url import URL


def show(body: str):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")


def load(url: URL):
    headers = Headers.default(url.host)
    requset = Request(url, headers=headers)

    http_client = HTTPClient(url)
    response = http_client.send_request(requset)

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
    show(response.body)
