import tkinter
import tkinter.font
from enum import Enum
from typing import List, Literal, Optional, Tuple, Union

from src.networking.cache import BrowserCache
from src.parser.parser_factory import ParserFactory
from src.render.tag import Tag
from src.render.text import Text
from src.resolver.resolver_factory import ResolverFactory
from src.utils.url import URL, AbstractURL

WIDTH = 800
HEIGHT = 600


SCROLL_STEP = 100

DEFUALT_FONT_SIZE = 16

FontWeight = Literal["normal", "bold"]
FontStyle = Literal["roman", "italic"]
DisplayList = List[Tuple[str, int, int, Optional[tkinter.font.Font]]]
BrowserContent = List[Union[Text, Tag]]


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
    url: Optional[AbstractURL]
    display_list: DisplayList
    scroll: int
    content: BrowserContent
    font: tkinter.font.Font
    weight: FontWeight
    style: FontStyle
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
        self.weight = "normal"
        self.style = "roman"
        self.HSTEP = self.font.measure(" ")
        self.VSTEP = self.font.metrics("linespace")
        self.url = None
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
        if (self.scroll + SCROLL_STEP) > self._get_highest_y_position() - SCROLL_STEP:
            return
        self.scroll += SCROLL_STEP
        self.draw()

    def _scroll_up(self, _: tkinter.Event):
        if (self.scroll - SCROLL_STEP) < 0:
            return
        self.scroll -= SCROLL_STEP
        self.draw()

    def _check_is_view_source(
        self,
    ) -> bool:
        return isinstance(self.url, URL) and self.url.is_view_source

    def _layout(self, tokens: BrowserContent) -> DisplayList:
        display_list: DisplayList = []
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        inside_body = False
        for token in tokens:
            if isinstance(token, Text) and (
                inside_body or self._check_is_view_source()
            ):
                cursor_x, cursor_y = self._layout_text(
                    token.text, cursor_x, cursor_y, self.font, display_list
                )
            elif isinstance(token, Tag):
                if token.tag == "body":
                    inside_body = True
                elif token.tag == "/body":
                    inside_body = False
                self._tag_style(token)
        return display_list

    def _tag_style(self, tag: Tag):
        if tag.tag == "i":
            self.style = "italic"
        elif tag.tag == "/i":
            self.style = "roman"
        elif tag.tag == "b":
            self.weight = "bold"
        elif tag.tag == "/b":
            self.weight = "normal"

        self.font = tkinter.font.Font(
            family="Times",
            size=self.font.actual()["size"],
            weight=self.weight,
            slant=self.style,
        )

    def _layout_text(
        self,
        word: str,
        cursor_x: int,
        cursor_y: int,
        font: tkinter.font.Font,
        display_list: DisplayList,
    ) -> Tuple[int, int]:
        # Only newlines
        if is_only_newlines(word):
            cursor_y += int(self.VSTEP * 1.25) * count_newlines(word)
            cursor_x = self.HSTEP
            return cursor_x, cursor_y

        word_size = self.font.measure(word)
        letter_size = int(word_size / len(word))

        # Line wrap
        if cursor_x + word_size > WIDTH - self.HSTEP:
            cursor_y += int(self.VSTEP * 1.25)
            cursor_x = self.HSTEP

        for c in word:
            if c == "\n":
                cursor_y += int(self.VSTEP * 1.25)
                cursor_x = self.HSTEP
                continue
            cursor_x += letter_size
            display_list.append((c, cursor_x, cursor_y, font))

        cursor_x += self.font.measure(" ")
        display_list.append((" ", cursor_x, cursor_y, font))
        return cursor_x, cursor_y

    def load(self, url: AbstractURL):
        self.url = url
        resolver = ResolverFactory.create(self.url, self.cache)
        parser = ParserFactory.create(resolver)
        self.content = parser.lex()
        self.display_list = self._layout(self.content)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for c, x, y, f in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f)

    def _get_highest_y_position(self) -> int:
        return self.display_list[-1][2]


def is_only_newlines(text: str) -> bool:
    return text.replace("\n", "") == ""


def count_newlines(text: str) -> int:
    return text.count("\n")
