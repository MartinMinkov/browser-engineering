import tkinter
import tkinter.font
from enum import Enum
from typing import List, Tuple, Union

from src.networking.cache import BrowserCache
from src.parser.parser_factory import ParserFactory
from src.render.tag import Tag
from src.render.text import Text
from src.resolver.resolver_factory import ResolverFactory
from src.utils.url import AbstractURL

WIDTH = 800
HEIGHT = 600


SCROLL_STEP = 100

DEFUALT_FONT_SIZE = 16


class WindowBindings(Enum):
    DOWN = "<Down>"
    UP = "<Up>"
    LEFT = "<Left>"
    RIGHT = "<Right>"
    SPACE = "<space>"
    SCROLL_UP = "<Button-4>"
    SCROLL_DOWN = "<Button-5>"
    RESIZE = "<Configure>"
    PLUS = "<plus>"
    MINUS = "<minus>"
    CTRL_D = "<Control-d>"

    def __str__(self):
        return self.value


class Browser:
    window: tkinter.Tk
    canvas: tkinter.Canvas
    cache: BrowserCache
    display_list: List[Tuple[str, int, int]]
    scroll: int
    content: List[Union[Text, Tag]]
    font: tkinter.font.Font
    HSTEP: int
    VSTEP: int

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.cache = BrowserCache()
        self.display_list = []
        self.scroll = 0
        self.content = ""
        self.font = tkinter.font.Font(family="Times", size=DEFUALT_FONT_SIZE)
        self.HSTEP = self.font.measure(" ")
        self.VSTEP = self.font.metrics("linespace")
        self._init_window_bindings()

    def _init_window_bindings(self):
        self.window.bind(str(WindowBindings.DOWN), self._scroll_down)
        self.window.bind(str(WindowBindings.UP), self._scroll_up)
        self.window.bind(str(WindowBindings.SCROLL_DOWN), self._scroll_down)
        self.window.bind(str(WindowBindings.SCROLL_UP), self._scroll_up)
        self.window.bind(str(WindowBindings.RESIZE), self._resize)
        self.window.bind(str(WindowBindings.PLUS), self._increase_font_size)
        self.window.bind(str(WindowBindings.MINUS), self._decrease_font_size)
        self.window.bind(str(WindowBindings.CTRL_D), self._close_window)

    def _close_window(self, _: tkinter.Event):
        self.window.destroy()

    def _increase_font_size(self, _: tkinter.Event):
        self.font = tkinter.font.Font(size=self.font.actual()["size"] + 1)
        self.HSTEP = self.HSTEP + 2
        self.display_list = self._layout(self.content)
        self.draw()

    def _decrease_font_size(self, _: tkinter.Event):
        self.font = tkinter.font.Font(size=self.font.actual()["size"] - 1)
        self.HSTEP = self.HSTEP - 2
        self.display_list = self._layout(self.content)
        self.draw()

    def _resize(self, event: tkinter.Event):
        global WIDTH, HEIGHT
        HEIGHT = event.height
        WIDTH = event.width
        self.display_list = self._layout(self.content)
        self.draw()

    def _scroll_down(self, _: tkinter.Event):
        if (self.scroll + SCROLL_STEP) > HEIGHT:
            return
        self.scroll += SCROLL_STEP
        self.draw()

    def _scroll_up(self, _: tkinter.Event):
        if (self.scroll - SCROLL_STEP) < 0:
            return
        self.scroll -= SCROLL_STEP
        self.draw()

    def _layout(self, tokens: List[Union[Text, Tag]]) -> List[Tuple[str, int, int]]:
        display_list: List[Tuple[str, int, int]] = []
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        for token in tokens:
            if isinstance(token, Text):
                cursor_x, cursor_y = self._layout_text_token(
                    token, cursor_x, cursor_y, display_list
                )
        return display_list

    def _layout_text_token(
        self,
        token: Text,
        cursor_x: int,
        cursor_y: int,
        display_list: List[Tuple[str, int, int]],
    ) -> Tuple[int, int]:
        for word in token.text.split():
            # Only newlines
            if is_only_newlines(word):
                cursor_y += int(self.VSTEP * 1.25) * count_newlines(word)
                cursor_x = self.HSTEP
                continue

            letter_size = int(self.font.measure(word) / len(word))
            # Line wrap
            if cursor_x + letter_size > WIDTH - self.HSTEP:
                cursor_y += int(self.VSTEP * 1.25)
                cursor_x = self.HSTEP

            for c in word:
                if c == "\n":
                    cursor_y += int(self.VSTEP * 1.25)
                    cursor_x = self.HSTEP
                    continue
                if c == "m" or c == "p":
                    cursor_x += self.font.measure(" ")

                cursor_x += letter_size
                display_list.append((c, cursor_x, cursor_y))

            cursor_x += self.font.measure(" ")
            display_list.append((" ", cursor_x, cursor_y))
        return cursor_x, cursor_y

    def load(self, url: AbstractURL):
        resolver = ResolverFactory.create(url, self.cache)
        parser = ParserFactory.create(resolver)
        document = parser.lex()
        self.content = document
        self.display_list = self._layout(document)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for c, x, y in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=self.font)


def is_only_newlines(text: str) -> bool:
    return text.replace("\n", "") == ""


def count_newlines(text: str) -> int:
    return text.count("\n")
