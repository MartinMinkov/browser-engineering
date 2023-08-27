from abc import ABC, abstractmethod
from enum import Enum


class Scheme(Enum):
    HTTP = "http"
    HTTPS = "https"
    File = "file"
    Data = "data"

    def __str__(self):
        return self.name.lower()


class AbstractURL(ABC):
    scheme: Scheme

    @abstractmethod
    def __init__(self, url: str):
        pass

    @abstractmethod
    def __str__(self):
        pass


class URL(AbstractURL):
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


class DataURL(AbstractURL):
    def __init__(self, url: str):
        scheme, url = url.split(":", 1)
        if scheme != Scheme.Data:
            raise ValueError("Invalid data URL")

        self.media_type = "text/plain;charset=US-ASCII"
        self.is_base64 = False

        if ";" in url:
            self.media_type, url = url.split(";", 1)

        if "base64" in url:
            self.is_base64 = True
            url = url.split(",", 1)[1]

        self.data = url

    def __str__(self):
        return f"{Scheme.Data}:{self.media_type},{self.data}"


class URLFactory:
    @staticmethod
    def create(url: str) -> AbstractURL:
        if url.startswith(str(Scheme.Data)):
            return DataURL(url)
        else:
            return URL(url)
