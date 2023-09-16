import tkinter
import tkinter.font
from enum import Enum
from typing import Dict

from src.networking.cache import BrowserCache
from src.parser.html_parser import print_tree
from src.parser.parser_factory import ParserFactory
from src.render.layout import Layout
from src.render.settings import Settings
from src.resolver.resolver_factory import ResolverFactory
from src.utils.url import AbstractURL


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
    scroll: int
    layouts: Dict[AbstractURL, Layout]
    settings: Settings

    def __init__(self):
        self.settings = Settings()
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, width=self.settings.width, height=self.settings.height
        )
        self.layouts = {}
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.cache = BrowserCache()
        self._init_window_bindings()

    def _init_window_bindings(self):
        self.window.bind(str(WindowBindings.DOWN), self._scroll_down)
        self.window.bind(str(WindowBindings.UP), self._scroll_up)
        self.window.bind(str(WindowBindings.SCROLL_DOWN), self._scroll_down)
        self.window.bind(str(WindowBindings.SCROLL_UP), self._scroll_up)
        self.window.bind(str(WindowBindings.PLUS), self._increase_font_size)
        self.window.bind(str(WindowBindings.MINUS), self._decrease_font_size)
        self.window.bind(str(WindowBindings.CTRL_D), self._close_window)

        # TODO This really slows things down, should investigate why it's called so many times
        # self.window.bind(str(WindowBindings.RESIZE), self._resize)

    def _close_window(self, _: tkinter.Event):
        self.window.destroy()

    def _increase_font_size(self, _: tkinter.Event):
        for layout in self.layouts.values():
            layout.increase_font_size()

    def _decrease_font_size(self, _: tkinter.Event):
        for layout in self.layouts.values():
            layout.decrease_font_size()

    def _resize(self, event: tkinter.Event):
        self.settings.resize(event.width, event.height)
        for layout in self.layouts.values():
            layout.resize(self.settings.height, self.settings.width)

    def _scroll_down(self, _: tkinter.Event):
        for layout in self.layouts.values():
            layout.scroll_down()

    def _scroll_up(self, _: tkinter.Event):
        for layout in self.layouts.values():
            layout.scroll_up()

    def load(self, url: AbstractURL):
        resolver = ResolverFactory.create(url, self.cache)
        parser = ParserFactory.create(resolver)
        html_element = parser.lex()
        print_tree(html_element)
        self.layouts[url] = Layout(url, self.canvas, html_element, self.settings)
