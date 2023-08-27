import socket
import ssl

from src.networking.headers import Headers
from src.networking.request import Request
from src.networking.response import Response
from src.utils.url import URL, Scheme


class HTTPClient:
    def __init__(self, url: URL, encoding="utf8"):
        self.url = url
        self.encoding = encoding
        self.s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        if url.scheme == Scheme.HTTPS:
            ctx = ssl.create_default_context()
            self.s = ctx.wrap_socket(self.s, server_hostname=url.host)

    def send_request(self, request: Request):
        self.s.connect((self.url.host, self.url.port))
        self.s.send((str(request)).encode(self.encoding))
        response = self.parse_request()
        self.s.close()
        return response

    def parse_request(self):
        response = self.s.makefile("r", encoding=self.encoding, newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = Headers()
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers.add_header(header, value)

        response = Response(int(status), explanation, response_headers, response.read())
        return response
