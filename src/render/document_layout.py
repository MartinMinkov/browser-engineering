from typing import List, Optional

from src.render.html_element import HTMLElement
from src.render.layout import BlockLayout
from src.render.settings import Settings
from src.render.types import DisplayList


class DocumentLayout:
    node: HTMLElement
    parent: Optional[HTMLElement]
    children: List[HTMLElement]
    display_list: DisplayList
    settings: Settings

    def __init__(self, node: HTMLElement, settings: Settings):
        self.node = node
        self.parent = None
        self.children = []
        self.settings = settings

    def layout(self):
        child = BlockLayout(self.node, self, None, self.settings)
        self.children.append(child)
        child.layout()
        self.display_list = child.display_list
