SCROLL_STEP = 100
WIDTH = 800
HEIGHT = 600


class Settings:
    scroll_step: int
    width: int
    height: int

    def __init__(self):
        self.scroll_step = 100
        self.width = 800
        self.height = 600

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
