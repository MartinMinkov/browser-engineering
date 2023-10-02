import tkinter.font
from typing import List, Tuple

from src.render.element import Element
from src.render.html_element import HTMLElement
from src.render.settings import Settings
from src.render.text import Text
from src.render.types import DisplayList, FontStyle, FontWeight

TextLine = List[Tuple[str, int, tkinter.font.Font]]


class BlockLayout:
    element: HTMLElement
    parent: HTMLElement
    previous: HTMLElement
    children: List[HTMLElement]

    display_list: DisplayList
    line: TextLine

    font: tkinter.font.Font
    weight: FontWeight
    size: int
    style: FontStyle

    cursor_x: int
    cursor_y: int

    def __init__(
        self,
        element: HTMLElement,
        parent: HTMLElement,
        previous: HTMLElement,
        settings: Settings,
    ):
        self.element = element
        self.parent = parent
        self.previous = previous
        self.children = []

        self.settings = settings
        self.display_list = []
        self.line = []

        self.size = self.settings.default_font_size
        self.weight = self.settings.default_weight
        self.style = self.settings.default_style
        self.font = tkinter.font.Font(
            family="Times", size=self.size, weight=self.weight, slant=self.style
        )

        self.settings.window_height
        self.settings.window_width

        self.cursor_x = self.settings.HSTEP
        self.cursor_y = self.settings.VSTEP

    def layout(self):
        self.recurse(self.element)
        self.flush()

    def recurse(self, tree: HTMLElement):
        if isinstance(tree.element, Text):
            self.layout_text(tree.element.text)
        elif isinstance(tree.element, Element):
            self.open_tag(tree.element)
            for child in tree.element.children:
                self.recurse(HTMLElement(child))
            self.close_tag(tree.element)

    def flush(self):
        if not self.line or len(self.line) == 0:
            return
        metrics = [font.metrics() for _, _, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + (1.25 * max_ascent)
        for word, x, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((word, x, y, font))
        self.line = []
        self.cursor_x = self.settings.HSTEP
        self.cursor_y += int(self.settings.VSTEP * 1.25)

    def layout_text(
        self,
        token: str,
    ):
        whitespace_size = self.font.measure(" ")
        token_size = self.font.measure(token)
        words = token.split(" ")
        num_words = len(words)
        word_size = int(token_size / num_words)

        for word in words:
            if (
                self.cursor_x + word_size
                > self.settings.window_width - self.settings.HSTEP
            ):
                self.flush()
            self.line.append((word, self.cursor_x, self.font))
            self.cursor_x += word_size + whitespace_size

    def open_tag(self, element: Element):
        tag = element.tag
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()
        self.font = self.settings.get_font(self.size, self.weight, self.style)

    def close_tag(self, element: Element):
        tag = element.tag
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "br":
            self.flush()
        elif tag == "/p":
            self.flush()
            self.cursor_y += self.settings.VSTEP
        self.font = self.settings.get_font(self.size, self.weight, self.style)

    def increase_font_size(self):
        self.font = tkinter.font.Font(size=self.size + 1)
        self.display_list = self.layout(self.element)

    def decrease_font_size(self):
        self.font = tkinter.font.Font(size=self.size - 1)
        self.display_list = self.layout(self.element)
