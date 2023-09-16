from typing import List, Optional

from src.render.base_element import BaseElement


class Text(BaseElement):
    text: str
    parent: Optional[BaseElement]
    children: List[BaseElement]

    def __init__(
        self, text: str, parent: Optional[BaseElement], children: List[BaseElement]
    ):
        self.text = text
        self.parent = parent
        self.children = children

    def __str__(self):
        return f"Text({self.text})"
