from enum import Enum
from typing import List, Tuple, Union

from src.parser.parser import Parser
from src.render.attributes import Attributes
from src.render.element import Element
from src.render.html_element import HTMLElement
from src.render.text import Text
from src.resolver.file_resolver import FileResolver
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
    resolver: Union[HTTPResolver, FileResolver]
    unfinished_tags: List[HTMLElement]
    inside_tag: bool

    def __init__(self, resolver: Union[HTTPResolver, FileResolver]):
        self.resolver = resolver
        self.unfinished_tags = []
        self.inside_tag = False

    def lex(self) -> HTMLElement:
        document = self.resolver.resolve()
        transformed = self._transform(document)
        return self._parse(transformed)

    def _parse(self, document: str) -> HTMLElement:
        text_buffer = ""
        for char in document:
            if char == "<":
                self.inside_tag = True
                text_buffer = text_buffer.strip()
                if text_buffer:
                    self.add_text(text_buffer)
                text_buffer = ""
            elif char == ">":
                self.inside_tag = False
                text_buffer = text_buffer.strip()
                if text_buffer:
                    self.add_tag(text_buffer)
                text_buffer = ""
            else:
                text_buffer += char
        if not self.inside_tag and text_buffer:
            text_buffer = text_buffer.strip()
            if text_buffer:
                self.add_tag(text_buffer)
        return self.finish()

    def add_text(self, text: str):
        parent = self.unfinished_tags[-1]
        node = Text(text, parent.element, [])
        parent.element.children.append(node)

    def add_tag(self, tag: str):
        tag, attributes = self.get_attributes(tag)
        if tag.startswith("!"):
            # Ignore DOCTYPE and comments
            return
        if tag.startswith("/"):
            self.close_tag()
        elif HTMLElement.is_self_closing(tag):
            self.self_closing_tag(tag, attributes)
        else:
            self.add_tag_to_parent(tag)

    def close_tag(self):
        if len(self.unfinished_tags) == 1:
            return
        # Get the last unfinished tag
        node = self.unfinished_tags.pop()
        # Get the parent if it exists
        parent = self.unfinished_tags[-1] if self.unfinished_tags else None
        if parent:
            # Add it to the parent
            parent.element.children.append(node.element)

    def self_closing_tag(self, tag: str, attributes: Attributes = Attributes({})):
        # Get the last unfinished tag
        self_closing_parent = (
            self.unfinished_tags[-1].element if self.unfinished_tags else None
        )
        if self_closing_parent:
            # Create a new element
            self_closing_element = Element(tag, self_closing_parent, [], attributes)
            # Add it to the parent
            self_closing_parent.children.append(self_closing_element)

    def add_tag_to_parent(self, tag: str, attributes: Attributes = Attributes({})):
        # Get the last unfinished tag
        parent_element = (
            self.unfinished_tags[-1].element if self.unfinished_tags else None
        )
        # Create a new element with the parent
        element_tag = Element(tag, parent_element, [], attributes)
        # Add to the unfinished tags
        self.unfinished_tags.append(HTMLElement(element_tag))

    def get_attributes(self, text: str) -> Tuple[str, Attributes]:
        parts = text.split()
        tag = parts[0].lower()
        attributes = Attributes.from_tag(parts[1:])
        return tag, attributes

    def finish(self) -> HTMLElement:
        if len(self.unfinished_tags) == 0:
            self.add_tag("html")
        while len(self.unfinished_tags) > 1:
            node = self.unfinished_tags.pop()
            parent = self.unfinished_tags[-1]
            parent.element.children.append(node.element)
        return self.unfinished_tags.pop()

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


def print_tree(node: HTMLElement, indent: int = 0):
    print(" " * indent, node.element)
    for child in node.element.children:
        print_tree(HTMLElement(child), indent + 1)
