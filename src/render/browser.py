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
        body = view.view_load(self.cache)
        view.view_show(body)

        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi!")
