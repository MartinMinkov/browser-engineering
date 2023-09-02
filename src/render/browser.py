import tkinter
import tkinter.font
from enum import Enum
from typing import List, Tuple

from src.networking.cache import BrowserCache
from src.utils.url import AbstractURL
from src.view.view_factory import ViewFactory

WIDTH = 800
HEIGHT = 600


SCROLL_STEP = 100

DEFUALT_FONT_SIZE = 12


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
    content: str
    font: tkinter.font.Font
    HSTEP = 13
    VSTEP = 18

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.cache = BrowserCache()
        self.display_list = []
        self.scroll = 0
        self.content = ""
        self.font = tkinter.font.Font(size=DEFUALT_FONT_SIZE)
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
        self.window.bind(str())

    def _close_window(self, _: tkinter.Event):
        self.window.destroy()

    def _increase_font_size(self, _: tkinter.Event):
        self.font = tkinter.font.Font(size=self.font.actual()["size"] + 1)
        self.HSTEP = self.HSTEP + 2
        self.VSTEP = self.font.metrics("linespace")
        self.display_list = self._layout(self.content)
        self.draw()

    def _decrease_font_size(self, _: tkinter.Event):
        self.font = tkinter.font.Font(size=self.font.actual()["size"] - 1)
        self.HSTEP = self.HSTEP - 2
        self.VSTEP = self.font.metrics("linespace")
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

    def _layout(self, text: str) -> List[Tuple[str, int, int]]:
        display_list = []
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        for c in text:
            if c == "\n":
                cursor_x = self.HSTEP
                cursor_y += self.VSTEP
                continue
            cursor_x += self.HSTEP
            if cursor_x >= WIDTH - self.HSTEP:
                cursor_x = self.HSTEP
                cursor_y += self.VSTEP
            display_list.append((c, cursor_x, cursor_y))
        return display_list

    def load(self, url: AbstractURL):
        view = ViewFactory.create(url)
        document = view.view_load(self.cache)
        body = view.lex(document)
        self.content = body
        self.display_list = self._layout(body)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for c, x, y in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=self.font)
