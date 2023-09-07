from abc import ABC, abstractmethod

from src.networking.cache import BrowserCache


class Parser(ABC):
    @abstractmethod
    def view_load(self, cache: BrowserCache) -> str:
        pass

    @abstractmethod
    def lex(self, body: str) -> str:
        pass

    @abstractmethod
    def view_show(self, body: str):
        pass
