class Settings:
    default_font_size: int
    scroll_step: int
    width: int
    height: int

    def __init__(self):
        self.scroll_step = 100
        self.width = 800
        self.height = 600
        self.default_font_size = 16

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
