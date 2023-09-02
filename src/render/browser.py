import tkinter
from enum import Enum
from typing import List, Tuple

from src.networking.cache import BrowserCache
from src.utils.url import AbstractURL
from src.view.view_factory import ViewFactory

WIDTH = 800
HEIGHT = 600

HSTEP = 13
VSTEP = 18

SCROLL_STEP = 100


class WindowBindings(Enum):
    DOWN = "<Down>"
    UP = "<Up>"
    LEFT = "<Left>"
    RIGHT = "<Right>"
    SPACE = "<space>"
    SCROLL_UP = "<Button-4>"
    SCROLL_DOWN = "<Button-5>"
    RESIZE = "<Configure>"

    def __str__(self):
        return self.value


class Browser:
    window: tkinter.Tk
    canvas: tkinter.Canvas
    cache: BrowserCache
    display_list: List[Tuple[str, int, int]]
    scroll: int
    content: str

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.cache = BrowserCache()
        self.display_list = []
        self.scroll = 0
        self.content = ""
        self._init_window_bindings()

    def _init_window_bindings(self):
        self.window.bind(str(WindowBindings.DOWN), self._scroll_down)
        self.window.bind(str(WindowBindings.UP), self._scroll_up)
        self.window.bind(str(WindowBindings.SCROLL_DOWN), self._scroll_down)
        self.window.bind(str(WindowBindings.SCROLL_UP), self._scroll_up)
        self.window.bind(str(WindowBindings.RESIZE), self._resize)

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
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            if c == "\n":
                cursor_x = HSTEP
                cursor_y += VSTEP
                continue
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_x = HSTEP
                cursor_y += VSTEP
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
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)
