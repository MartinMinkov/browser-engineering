import socket
import ssl

from src.networking.headers import Headers
from src.networking.request import Request
from src.networking.response import Response
from src.utils.url import URL, Scheme

REDIRECT_STATUSES = {301, 302}

MAX_REDIRECT_COUNT = 10


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
        s.connect((self.url.host, self.url.port))
        return s

    def _parse_redirect(self, response: Response) -> URL:
        location = response.headers.get_header("location")
        if location.startswith("/"):
            return URL(f"{self.url.scheme}://{self.url.host}{location}")
        else:
            return URL(location)

    def _handle_redirect(self, response: Response) -> Response:
        for _ in range(MAX_REDIRECT_COUNT):
            if response.status_code not in REDIRECT_STATUSES:
                break
            else:
                self.s.close()
                self.url = self._parse_redirect(response)
                self.s = self._create_socket()
                request = Request(self.url, headers=response.headers)
                self.s.send((str(request)).encode(self.encoding))
                response = self._parse_response()
        if response.status_code in REDIRECT_STATUSES:
            raise Exception("Too many redirects")
        return response

    def send_request(self, request: Request) -> Response:
        self.s.send((str(request)).encode(self.encoding))
        response = self._parse_response()

        if response.status_code in REDIRECT_STATUSES:
            response = self._handle_redirect(response)

        self.s.close()
        return response

    def _parse_response(self) -> Response:
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
