from typing import List, Union

from src.parser.parser import Parser
from src.render.tag import Tag
from src.render.text import Text
from src.resolver.file_resolver import FileResolver


class FileParser(Parser):
    resolver: FileResolver

    def __init__(self, resolver: FileResolver):
        self.resolver = resolver

    def lex(self) -> List[Union[Text, Tag]]:
        return [Text(self.resolver.resolve())]
