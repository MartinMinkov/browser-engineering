from enum import Enum


class Scheme(Enum):
    HTTP = "http"
    HTTPS = "https"
    File = "file"

    def __str__(self):
        return self.name.lower()


class URL:
    def __init__(self, url: str):
        scheme, url = url.split("://", 1)
        self.scheme = Scheme(scheme)

        if self.scheme == Scheme.HTTP:
            self.port = 80
        elif self.scheme == Scheme.HTTPS:
            self.port = 443

        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.path = "/" + url

    def __str__(self):
        return f"{self.scheme}://{self.host}:{self.port}{self.path}"
