from typing import List, Union

from src.parser.parser import Parser
from src.render.tag import Tag
from src.render.text import Text
from src.resolver.data_resolver import DataResolver


class DataParser(Parser):
    resolver: DataResolver

    def __init__(self, resolver: DataResolver):
        self.resolver = resolver

    def lex(self) -> List[Union[Text, Tag]]:
        return [Text(self.resolver.resolve())]
