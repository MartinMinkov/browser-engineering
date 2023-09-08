from enum import Enum
from typing import List, Union

from src.parser.parser import Parser
from src.render.tag import Tag
from src.render.text import Text
from src.resolver.http_resolver import HTTPResolver


class HTMLEntity(Enum):
    GreaterThan = ("&gt;", ">")
    LessThan = ("&lt;", "<")
    Amperstand = ("&amp;", "&")
    Dash = ("&dash;", "-")
    NDash = ("&ndash;", "–")
    MDash = ("&mdash;", "—")
    Copy = ("&copy;", "©")

    def conatins(self, value: str) -> bool:
        return value in self.value

    def __str__(self):
        return self.value[0]

    def symbol(self):
        return self.value[1]


class HTMLParser(Parser):
    resolver: HTTPResolver
    inside_tag: bool

    def __init__(self, resolver: HTTPResolver):
        self.resolver = resolver
        self.inside_tag = False

    def lex(self) -> List[Union[Text, Tag]]:
        document = self.resolver.resolve()
        if self.resolver.url.is_view_source:
            return [Text(document)]
        transformed = self._transform(document)
        return self._body(transformed)

    def _body(self, document: str) -> List[Union[Text, Tag]]:
        tokens: List[Union[Text, Tag]] = []
        text_buffer = ""
        for char in document:
            if char == "<":
                self.inside_tag = True
                if text_buffer:
                    tokens.append(Text(text_buffer))
                text_buffer = ""
            elif char == ">":
                self.inside_tag = False
                tokens.append(Tag(text_buffer))
                text_buffer = ""
            else:
                text_buffer += char
        if not self.inside_tag and text_buffer:
            tokens.append(Text(text_buffer))
        return tokens

    def _transform(self, document: str) -> str:
        transformed_document = ""
        idx = 0
        while idx < len(document):
            if document[idx] == "&":
                for entity in HTMLEntity:
                    if entity.conatins(document[idx : idx + len(str(entity))]):
                        transformed_document += entity.symbol()
                        idx += len(str(entity))
                        break
            transformed_document += document[idx]
            idx += 1
        return transformed_document

    def _is_start_of_tag(self, document: str, idx: int, tag: str) -> bool:
        return document[idx : idx + len(tag) + 1] == f"<{tag}"
