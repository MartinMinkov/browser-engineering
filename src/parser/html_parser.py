from enum import Enum

from src.parser.parser import Parser
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
    inside_body_tag: bool
    in_angle_brackets: bool

    def __init__(self, resolver: HTTPResolver):
        self.resolver = resolver
        self.inside_body_tag = False
        self.in_angle_brackets = False

    def lex(self) -> str:
        document = self.resolver.resolve()
        body = self._body(document)
        return self._transform(body)

    def _body(self, document: str) -> str:
        body_document = ""
        for idx, char in enumerate(document):
            if char == "<":
                if self._is_start_of_tag(document, idx, "body"):
                    self.inside_body_tag = True
                elif self._is_start_of_tag(document, idx, "/body"):
                    self.inside_body_tag = False
                self.in_angle_brackets = True
            elif char == ">":
                self.in_angle_brackets = False
            elif self.inside_body_tag and not self.in_angle_brackets:
                body_document += char
        return body_document

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
