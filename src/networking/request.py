from src.networking.headers import Headers
from src.utils.url import URL


class Request:
    def __init__(
        self,
        url: URL,
        headers: Headers,
        method: str = "GET",
    ):
        self.url = url
        self.headers = headers
        self.method = method

    def __str__(self):
        return "{} {} HTTP/1.0\r\n{}\r\n\r\n".format(
            self.method, self.url.path, self.headers
        )
