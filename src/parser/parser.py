from abc import ABC, abstractmethod
from typing import List

from src.render.html_element import HTMLElement


class Parser(ABC):
    @abstractmethod
    def lex(self) -> HTMLElement:
        """
        Lex the source data and return a tree of HTMLElements.

        The method processes the input source, tokenizes it, and structures it
        into a tree of HTMLElements that represents the content structure.

        Returns:
            HTMLElement: The root of the parsed HTMLElement tree.

        Note:
            This method must be implemented by subclasses.
        """
        pass
