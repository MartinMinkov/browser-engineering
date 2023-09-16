from typing import List

from src.parser.parser import Parser
from src.render.html_element import HTMLElement
from src.render.text import Text
from src.resolver.data_resolver import DataResolver


class DataParser(Parser):
    resolver: DataResolver

    def __init__(self, resolver: DataResolver):
        self.resolver = resolver

    def lex(self) -> HTMLElement:
        return HTMLElement(Text(self.resolver.resolve(), None, []))
