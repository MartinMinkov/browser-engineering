import tkinter.font
from typing import Dict, Tuple

from src.render.types import FontStyle, FontWeight


class Settings:
    default_font_size: int
    scroll_step: int
    window_width: int
    window_height: int
    default_weight: FontWeight
    defalt_style: FontStyle

    HSTEP: int
    VSTEP: int

    font_cache: Dict[Tuple[str, str, int], tkinter.font.Font]

    def __init__(self):
        self.scroll_step = 100
        self.window_width = 800
        self.window_height = 600

        self.default_font_size = 16
        self.default_weight = "normal"
        self.default_style = "roman"

        self.HSTEP = 30
        self.VSTEP = tkinter.font.Font(
            family="Times",
            size=self.default_font_size,
            weight=self.default_weight,
            slant=self.default_style,
        ).metrics("linespace")
        self.font_cache = {}

    def resize(self, width: int, height: int):
        self.window_width = width
        self.window_height = height

    def increase_font_size(self):
        self.HSTEP = self.HSTEP + 2

    def decrease_font_size(self):
        self.HSTEP = self.HSTEP - 2

    def set_font(self, size: int, font_weight: FontWeight, slant: FontStyle):
        self.size = size
        self.weight = font_weight
        self.style = slant
        self.font = tkinter.font.Font(
            family="Times",
            size=size,
            weight=font_weight,
            slant=slant,
        )

    def get_font(
        self, size: int, font_weight: FontWeight, slant: FontStyle
    ) -> tkinter.font.Font:
        key = (font_weight, slant, size)
        if key not in self.font_cache:
            self.font_cache[key] = tkinter.font.Font(
                family="Times",
                size=size,
                weight=font_weight,
                slant=slant,
            )
        return self.font_cache[key]
