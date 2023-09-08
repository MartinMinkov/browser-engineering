from abc import ABC, abstractmethod
from typing import List, Union

from src.render.tag import Tag
from src.render.text import Text


class Parser(ABC):
    @abstractmethod
    def lex(self) -> List[Union[Text, Tag]]:
        pass
