import re
import tkinter.font
from typing import List, Literal, Optional, Tuple, Union

from src.render.settings import Settings
from src.render.tag import Tag
from src.render.text import Text
from src.utils.url import URL, AbstractURL

FontWeight = Literal["normal", "bold"]
FontStyle = Literal["roman", "italic"]
DisplayList = List[Tuple[str, int, int, tkinter.font.Font]]
BrowserContent = List[Union[Text, Tag]]
TextLine = List[Tuple[str, int, tkinter.font.Font]]


class Layout:
    display_list: DisplayList
    line: TextLine
    url: Optional[AbstractURL]

    font: tkinter.font.Font
    weight: FontWeight
    size: int
    style: FontStyle
    content: BrowserContent

    window_height: int
    window_width: int
    cursor_x: int
    cursor_y: int
    HSTEP: int
    VSTEP: int
    scroll: int

    def __init__(
        self,
        url: AbstractURL,
        canvas: tkinter.Canvas,
        tokens: BrowserContent,
        settings: Settings,
    ):
        self.content = tokens
        self.url = url
        self.settings = settings
        self.canvas = canvas
        self.display_list = []
        self.line = []

        self.size = self.settings.default_font_size
        self.weight = "normal"
        self.style = "roman"
        self.font = tkinter.font.Font(
            family="Times", size=self.size, weight=self.weight, slant=self.style
        )

        self.scroll = 0
        self.window_height = self.settings.height
        self.window_width = self.settings.width
        self.HSTEP = self.font.measure(" ")
        self.VSTEP = self.font.metrics("linespace")
        self.cursor_x = self.HSTEP
        self.cursor_y = self.VSTEP

        self._layout(tokens)
        self.flush()
        self.draw()

    def _layout(self, tokens: BrowserContent):
        inside_body = False
        for token in tokens:
            if isinstance(token, Text) and (
                inside_body or self._check_is_view_source()
            ):
                for word in split_words_with_indentation(token.text):
                    self._layout_text(
                        word,
                    )
            elif isinstance(token, Tag):
                if "body" in token.tag:
                    inside_body = True
                elif "/body" in token.tag:
                    inside_body = False
                self._tag_style(token)

    def resize(self, height: int, width: int):
        self.window_height = height
        self.window_width = width
        self.draw()

    def flush(self):
        if not self.line or len(self.line) == 0:
            return
        metrics = [font.metrics() for _, _, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + (1.25 * max_ascent)
        for word, x, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((word, x, y, font))
        self.cursor_x = self.HSTEP
        self.cursor_y += int(self.VSTEP * 1.25)
        self.line = []

    def _layout_text(
        self,
        word: str,
    ):
        # Only newlines
        if is_only_newlines(word):
            self.cursor_y += int(self.VSTEP * 1.25) * count_newlines(word)
            self.cursor_x = self.HSTEP

        word_size = self.font.measure(word)
        # Line wrap
        if self.cursor_x + word_size > self.window_width - self.HSTEP:
            self.flush()

        self.cursor_x += word_size
        self.line.append((word, self.cursor_x, self.font))

    def _tag_style(self, tag: Tag):
        t = tag.tag
        if t == "i":
            self.style = "italic"
        elif t == "/i":
            self.style = "roman"
        elif t == "b":
            self.weight = "bold"
        elif t == "/b":
            self.weight = "normal"
        elif t == "small":
            self.size -= 2
        elif t == "/small":
            self.size += 2
        elif t == "big":
            self.size += 4
        elif t == "/big":
            self.size -= 4
        elif t == "br":
            self.flush()
        elif t == "/p":
            self.flush()
            self.cursor_y += self.VSTEP

        self.font = tkinter.font.Font(
            family="Times",
            size=self.font.actual()["size"],
            weight=self.weight,
            slant=self.style,
        )

    def increase_font_size(self):
        self.font = tkinter.font.Font(size=self.font.actual()["size"] + 1)
        self.HSTEP = self.HSTEP + 2
        self.display_list = self._layout(self.content)
        self.draw()

    def decrease_font_size(self):
        self.font = tkinter.font.Font(size=self.font.actual()["size"] - 1)
        self.HSTEP = self.HSTEP - 2
        self.display_list = self._layout(self.content)
        self.draw()

    def scroll_down(self):
        if (
            self.scroll + self.settings.scroll_step
        ) > self._get_highest_y_position() - self.settings.scroll_step:
            return
        self.scroll += self.settings.scroll_step
        self.draw()

    def scroll_up(self):
        if (self.scroll - self.settings.scroll_step) < 0:
            return
        self.scroll -= self.settings.scroll_step
        self.draw()

    def _check_is_view_source(self) -> bool:
        return isinstance(self.url, URL) and self.url.is_view_source

    def _get_highest_y_position(self) -> int:
        return self.display_list[-1][2]

    def draw(self):
        self.canvas.delete("all")
        for c, x, y, f in self.display_list:
            if y > self.scroll + self.window_height:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f)


def is_only_newlines(text: str) -> bool:
    return text.replace("\n", "") == ""


def count_newlines(text: str) -> int:
    return text.count("\n")


def split_words_with_indentation(text: str) -> List[str]:
    words = re.findall(r"(\s*\S+)", text)
    return words
