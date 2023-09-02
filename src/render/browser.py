import tkinter

from src.networking.cache import BrowserCache
from src.utils.url import AbstractURL
from src.view.view_factory import ViewFactory

WIDTH = 800
HEIGHT = 600


class Browser:
    window: tkinter.Tk
    canvas: tkinter.Canvas
    cache: BrowserCache

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.cache = BrowserCache()

    def load(self, url: AbstractURL):
        view = ViewFactory.create(url)
        document = view.view_load(self.cache)
        body = view.lex(document)

        HSTEP, VSTEP = 13, 18
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in body:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_x = HSTEP
                cursor_y += VSTEP
