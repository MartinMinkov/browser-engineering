import socket
import ssl
from src.utils.headers import Headers
from src.utils.request import Request


class URL:
    def __init__(self, url: str):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"], "Invalid URL scheme"

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.path = "/" + url

    def request(self):
        s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        socket_request = Request(self.path, "GET", Headers.default(self.host))
        s.connect((self.host, self.port))
        s.send((str(socket_request)).encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        assert status == "200", "{}: {}".format(status, explanation)

        response_headers = Headers()
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers.add_header(header, value)
            assert "transfer-encoding" not in response_headers.headers
            assert "content-encoding" not in response_headers.headers

        encoding = "utf8"
        if (
            "content-type" in response_headers.headers
            and "charset=" in response_headers.get_header("content-type")
        ):
            encoding = response_headers.get_header("content-type").split("charset=")[-1]

        body = response.read()
        s.close()
        return response_headers, body
