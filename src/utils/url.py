import socket
import ssl
from src.utils.headers import Headers


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

        s.connect((self.host, self.port))
        s.send(
            (
                "GET {} HTTP/1.0\r\n".format(self.path)
                + "Host: {}\r\n\r\n".format(self.host)
            ).encode("utf8")
        )

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        assert status == "200", "{}: {}".format(status, explanation)

        headers = Headers()
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            headers.add_header(header, value)
            assert "transfer-encoding" not in headers.headers
            assert "content-encoding" not in headers.headers

        encoding = "utf8"
        if "content-type" in headers.headers and "charset=" in headers.get_header(
            "content-type"
        ):
            encoding = headers.get_header("content-type").split("charset=")[-1]

        body = response.read()
        s.close()
        return headers, body
