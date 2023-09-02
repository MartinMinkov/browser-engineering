import tkinter
from typing import List, Tuple

from src.networking.cache import BrowserCache
from src.utils.url import AbstractURL
from src.view.view_factory import ViewFactory

WIDTH = 800
HEIGHT = 600

HSTEP = 13
VSTEP = 18


class Browser:
    window: tkinter.Tk
    canvas: tkinter.Canvas
    cache: BrowserCache
    display_list: List[Tuple[str, int, int]]
    scroll: int

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.cache = BrowserCache()
        self.display_list = []
        self.scroll = 0

    def _layout(self, text: str) -> List[Tuple[str, int, int]]:
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            display_list.append((c, cursor_x, cursor_y))
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_x = HSTEP
                cursor_y += VSTEP
        return display_list

    def load(self, url: AbstractURL):
        view = ViewFactory.create(url)
        document = view.view_load(self.cache)
        body = view.lex(document)
        self.display_list = self._layout(body)
        self.draw()

    def draw(self):
        for c, x, y in self.display_list:
            self.canvas.create_text(x, y - self.scroll, text=c)
