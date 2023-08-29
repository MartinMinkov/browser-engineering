from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Tuple


class Scheme(Enum):
    HTTP = "http"
    HTTPS = "https"
    File = "file"
    Data = "data"
    ViewSource = "view-source"

    def __str__(self):
        return self.value.lower()


class AbstractURL(ABC):
    scheme: Scheme

    @abstractmethod
    def __init__(self, url: str):
        pass

    @abstractmethod
    def __str__(self):
        pass


class URL(AbstractURL):
    DEFAULT_PORTS: Dict[Scheme, int] = {
        Scheme.HTTP: 80,
        Scheme.HTTPS: 443,
    }

    is_view_source: bool
    scheme: Scheme
    host: str
    path: str
    port: int

    def __init__(self, url: str):
        self.is_view_source = False

        url = self._handle_view_source(url)
        self.scheme, url = self._extract_scheme(url)
        self.host, self.path = self._extract_host_and_path(url)

    def _handle_view_source(self, url: str) -> str:
        if str(Scheme.ViewSource) in url:
            self.is_view_source = True
            url = url.replace(str(Scheme.ViewSource) + ":", "")
        return url

    def _extract_scheme(self, url: str) -> Tuple[Scheme, str]:
        scheme_str, url = url.split("://", 1)
        scheme = Scheme(scheme_str)
        self.port = self.DEFAULT_PORTS[scheme]
        return scheme, url

    def _extract_host_and_path(self, url: str) -> Tuple[str, str]:
        if "/" not in url:
            url += "/"
        host, path = url.split("/", 1)
        if ":" in host:
            host, port = host.split(":", 1)
            self.port = int(port)
        return host, "/" + path

    def __str__(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}{self.path}"


class DataURL(AbstractURL):
    scheme: Scheme
    media_type: str
    is_base64: bool
    data: str

    DEFAULT_MEDIA_TYPE = "text/plain;charset=US-ASCII"

    def __init__(self, url: str):
        self.scheme, rest_of_url = self._extract_scheme(url)
        if self.scheme != Scheme.Data:
            raise ValueError("Invalid data URL")

        self.media_type, rest_of_data = self._extract_media_type(rest_of_url)
        self.is_base64 = "base64" in rest_of_data
        self.data = self._extract_data(rest_of_data)

    def _extract_scheme(self, url: str) -> Tuple[Scheme, str]:
        scheme_str, rest_of_url = url.split(":", 1)
        return Scheme(scheme_str), rest_of_url

    def _extract_media_type(self, url: str) -> Tuple[str, str]:
        if ";" in url:
            media_type, rest_of_data = url.split(";", 1)
            return media_type, rest_of_data
        return self.DEFAULT_MEDIA_TYPE, url

    def _extract_data(self, url: str) -> str:
        return url.split(",", 1)[1]

    def __str__(self) -> str:
        return f"{self.scheme}:{self.media_type},{self.data}"


class URLFactory:
    @staticmethod
    def create(url: str) -> AbstractURL:
        if url.startswith(str(Scheme.Data)):
            return DataURL(url)
        else:
            return URL(url)
