import socket
import ssl

from src.utils.headers import Headers
from src.utils.request import Request
from src.utils.response import Response
from src.utils.url import URL


class HTTPClient:
    def __init__(self, url: URL):
        self.url = url
        self.s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        if url.scheme == "https":
            ctx = ssl.create_default_context()
            self.s = ctx.wrap_socket(self.s, server_hostname=url.host)

    def send_request(self, request: Request):
        self.s.connect((self.url.host, self.url.port))
        self.s.send((str(request)).encode("utf8"))
        response = self.parse_request()
        self.s.close()
        return response

    def parse_request(self):
        response = self.s.makefile("r", encoding="utf8", newline="\r\n")
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
