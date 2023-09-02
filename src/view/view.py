from abc import ABC, abstractmethod

from src.networking.cache import BrowserCache


class View(ABC):
    @abstractmethod
    def view_load(self, cache: BrowserCache) -> str:
        pass

    @abstractmethod
    def view_show(self, body: str):
        pass
