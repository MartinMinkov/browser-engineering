from abc import ABC, abstractmethod


class View(ABC):
    @abstractmethod
    def load(self) -> str:
        pass

    @abstractmethod
    def show(self, body: str):
        pass
