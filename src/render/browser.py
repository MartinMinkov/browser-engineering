import tkinter
import tkinter.font
from enum import Enum

from src.networking.cache import BrowserCache
from src.parser.html_parser import print_tree
from src.parser.parser_factory import ParserFactory
from src.render.document_layout import DocumentLayout
from src.render.layout import BlockLayout, DisplayList
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
    document: DocumentLayout
    display_list: DisplayList

    scroll: int
    settings: Settings

    def __init__(self):
        self.window = tkinter.Tk()
        self.settings = Settings()
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.settings.window_width,
            height=self.settings.window_height,
        )

        self.scroll = 0
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

    def load(self, url: AbstractURL):
        resolver = ResolverFactory.create(url, self.cache)
        parser = ParserFactory.create(resolver)
        nodes = parser.lex()
        print_tree(nodes)

        self.document = DocumentLayout(nodes, self.settings)
        self.document.layout()
        self.display_list = self.document.display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for c, x, y, f in self.display_list:
            if y > self.scroll + self.settings.window_height:
                continue
            if y + self.settings.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f)

    def _close_window(self, _: tkinter.Event):
        self.window.destroy()

    def _increase_font_size(self, _: tkinter.Event):
        self.settings.increase_font_size()
        self.document.increase_font_size()
        self.display_list = self.document.display_list
        self.draw()

    def _decrease_font_size(self, _: tkinter.Event):
        self.settings.decrease_font_size()
        self.document.decrease_font_size()
        self.display_list = self.document.display_list
        self.draw()

    def _resize(self, event: tkinter.Event):
        if (self.settings.window_height == event.height) and (
            self.settings.window_width == event.width
        ):
            return
        self.settings.resize(event.width, event.height)
        self.draw()

    def _scroll_down(self, _: tkinter.Event):
        if (
            self.scroll + self.settings.scroll_step
        ) > self._get_highest_y_position() - self.settings.scroll_step:
            return
        self.scroll += self.settings.scroll_step
        self.draw()

    def _scroll_up(self, _: tkinter.Event):
        if (self.scroll - self.settings.scroll_step) < 0:
            return
        self.scroll -= self.settings.scroll_step
        self.draw()

    def _get_highest_y_position(self) -> int:
        return self.display_list[-1][2]
