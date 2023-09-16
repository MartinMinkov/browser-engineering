import re
import tkinter.font
from typing import Dict, List, Literal, Optional, Tuple

from src.render.element import Element
from src.render.html_element import HTMLElement
from src.render.settings import Settings
from src.render.text import Text
from src.utils.url import URL, AbstractURL

FontWeight = Literal["normal", "bold"]
FontStyle = Literal["roman", "italic"]
DisplayList = List[Tuple[str, int, int, tkinter.font.Font]]
TextLine = List[Tuple[str, int, tkinter.font.Font]]


class Layout:
    display_list: DisplayList
    line: TextLine
    url: Optional[AbstractURL]

    font_cache: Dict[Tuple[FontWeight, FontStyle, int], tkinter.font.Font]
    font: tkinter.font.Font
    weight: FontWeight
    size: int
    style: FontStyle
    content: HTMLElement

    window_height: int
    window_width: int
    cursor_x: int
    cursor_y: int
    HSTEP: int
    VSTEP: int
    scroll: int

    def __init__(
        self,
        url: AbstractURL,
        canvas: tkinter.Canvas,
        element: HTMLElement,
        settings: Settings,
    ):
        self.content = element
        self.url = url
        self.settings = settings
        self.canvas = canvas
        self.display_list = []
        self.line = []

        self.size = self.settings.default_font_size
        self.weight = "normal"
        self.style = "roman"
        self.font = tkinter.font.Font(
            family="Times", size=self.size, weight=self.weight, slant=self.style
        )
        self.font_cache = {}

        self.scroll = 0
        self.window_height = self.settings.height
        self.window_width = self.settings.width
        self.HSTEP = 30
        self.VSTEP = self.font.metrics("linespace")
        self.cursor_x = self.HSTEP
        self.cursor_y = self.VSTEP

        self.recurse(element)
        self.flush()
        self.draw()

    def recurse(self, tree: HTMLElement):
        if isinstance(tree.element, Text):
            self._layout_text(tree.element.text)
        elif isinstance(tree.element, Element):
            self.open_tag(tree.element)
            for child in tree.element.children:
                self.recurse(HTMLElement(child))
            self.close_tag(tree.element)

    def resize(self, height: int, width: int):
        if (self.window_height == height) and (self.window_width == width):
            return
        self.window_height = height
        self.window_width = width
        self.recurse(self.content)
        self.draw()

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
        self.cursor_x = self.HSTEP
        self.cursor_y += int(self.VSTEP * 1.25)

    def _layout_text(
        self,
        token: str,
    ):
        whitespace_size = self.font.measure(" ")
        token_size = self.font.measure(token)
        words = token.split(" ")
        num_words = len(words)

        for word in words:
            word_size = int(token_size / num_words)
            if self.cursor_x + word_size > self.window_width - self.HSTEP:
                self.flush()

            self.line.append((word, self.cursor_x, self.font))
            self.cursor_x += word_size + whitespace_size

    def draw(self):
        self.canvas.delete("all")
        for c, x, y, f in self.display_list:
            if y > self.scroll + self.window_height:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f)

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
        self.font = self.get_font(self.size, self.weight, self.style)

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
            self.cursor_y += self.VSTEP
        self.font = self.get_font(self.size, self.weight, self.style)

    def increase_font_size(self):
        self.font = tkinter.font.Font(size=self.size + 1)
        self.HSTEP = self.HSTEP + 2
        self.display_list = self._layout(self.content)
        self.draw()

    def decrease_font_size(self):
        self.font = tkinter.font.Font(size=self.size - 1)
        self.HSTEP = self.HSTEP - 2
        self.display_list = self._layout(self.content)
        self.draw()

    def scroll_down(self):
        if (
            self.scroll + self.settings.scroll_step
        ) > self._get_highest_y_position() - self.settings.scroll_step:
            return
        self.scroll += self.settings.scroll_step
        self.draw()

    def scroll_up(self):
        if (self.scroll - self.settings.scroll_step) < 0:
            return
        self.scroll -= self.settings.scroll_step
        self.draw()

    def _check_is_view_source(self) -> bool:
        return isinstance(self.url, URL) and self.url.is_view_source

    def _get_highest_y_position(self) -> int:
        return self.display_list[-1][2]

    def get_font(
        self, size: int, font_weight: FontWeight, slant: FontStyle
    ) -> tkinter.font.Font:
        key = (font_weight, slant, size)
        if key not in self.font_cache:
            self.font_cache[key] = tkinter.font.Font(
                family="Times",
                size=self.size,
                weight=self.weight,
                slant=self.style,
            )
        return self.font_cache[key]


def is_only_newlines(text: str) -> bool:
    return text.replace("\n", "") == ""


def count_newlines(text: str) -> int:
    return text.count("\n")


def split_words_with_indentation(text: str) -> List[str]:
    words = re.findall(r"(\s*\S+)", text)
    return words
