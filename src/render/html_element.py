from dataclasses import dataclass

from src.render.base_element import BaseElement

SELF_CLOSING_TAGS = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
]


@dataclass
class HTMLElement:
    element: BaseElement

    def __str__(self):
        return f"HTMLElement({self.element})"

    @staticmethod
    def is_self_closing(tag: str) -> bool:
        return tag in SELF_CLOSING_TAGS
