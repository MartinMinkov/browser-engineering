from abc import ABC, abstractmethod


class View(ABC):
    @abstractmethod
    def view_load(self) -> str:
        pass

    @abstractmethod
    def view_show(self, body: str):
        pass
