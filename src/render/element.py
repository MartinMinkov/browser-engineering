from typing import List, Optional

from src.render.attributes import Attributes
from src.render.base_element import BaseElement


class Element(BaseElement):
    tag: str
    parent: Optional[BaseElement]
    children: List[BaseElement]
    attributes: Optional[Attributes]

    def __init__(
        self,
        tag: str,
        parent: Optional[BaseElement],
        children: List[BaseElement],
        attributes: Optional[Attributes],
    ):
        self.tag = tag
        self.parent = parent
        self.children = children
        self.attributes = attributes

    def __str__(self):
        attributes_str = (
            " " + str(self.attributes) if self.attributes.size() > 0 else ""
        )
        return "<" + self.tag + attributes_str + ">"
