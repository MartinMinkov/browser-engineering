from pathlib import Path
from typing import List, Union

from src.parser.html_parser import HTMLParser
from src.parser.parser import Parser
from src.render.tag import Tag
from src.render.text import Text
from src.resolver.file_resolver import FileResolver


class FileParser(Parser):
    resolver: FileResolver

    def __init__(self, resolver: FileResolver):
        self.resolver = resolver

    def lex(self) -> List[Union[Text, Tag]]:
        if Path(self.resolver.url.path).suffix == ".html":
            # If we have a .html document, we just use the HTML parser to lex it.
            return HTMLParser(self.resolver).lex()
        return [Text(self.resolver.resolve())]
