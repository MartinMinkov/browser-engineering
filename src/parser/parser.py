from abc import ABC, abstractmethod

from src.networking.cache import BrowserCache


class Parser(ABC):
    @abstractmethod
    def lex(self) -> str:
        pass
