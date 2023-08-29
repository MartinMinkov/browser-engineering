import socket
import ssl

from src.networking.headers import Headers
from src.networking.request import Request
from src.networking.response import Response
from src.utils.url import URL, Scheme


class HTTPClient:
    url: URL
    encoding: str
    s: socket.socket

    def __init__(self, url: URL, encoding: str = "utf8"):
        self.url = url
        self.encoding = encoding
        self.s = self._create_socket()

    def _create_socket(self) -> socket.socket:
        s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        if self.url.scheme == Scheme.HTTPS:
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.url.host)
        return s

    def send_request(self, request: Request) -> Response:
        self.s.connect((self.url.host, self.url.port))
        self.s.send((str(request)).encode(self.encoding))
        response = self._parse_request()
        self.s.close()
        return response

    def _parse_request(self) -> Response:
        response_file = self.s.makefile("r", encoding=self.encoding, newline="\r\n")
        statusline = response_file.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = self._read_headers(response_file)

        response = Response(
            int(status), explanation, response_headers, response_file.read()
        )
        return response

    def _read_headers(self, response_file) -> Headers:
        headers = Headers()
        while True:
            line = response_file.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            headers.add_header(header.strip(), value.strip())
        return headers
