import re
import tkinter.font
from typing import List, Literal, Optional, Tuple, Union

from src.render.settings import Settings
from src.render.tag import Tag
from src.render.text import Text
from src.utils.url import URL, AbstractURL

FontWeight = Literal["normal", "bold"]
FontStyle = Literal["roman", "italic"]
DisplayList = List[Tuple[str, int, int, Optional[tkinter.font.Font]]]
BrowserContent = List[Union[Text, Tag]]


DEFUALT_FONT_SIZE = 16


class Layout:
    display_list: DisplayList
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

        self.size = DEFUALT_FONT_SIZE
        self.weight = "normal"
        self.style = "roman"
        self.font = tkinter.font.Font(family="Times", size=self.size)

        self.scroll = 0
        self.window_height = self.settings.height
        self.window_width = self.settings.width
        self.HSTEP = self.font.measure(" ")
        self.VSTEP = self.font.metrics("linespace")
        self.cursor_x = self.HSTEP
        self.cursor_y = self.VSTEP

        self.display_list = self._layout(tokens)
        self.draw()

    def _layout(self, tokens: BrowserContent) -> DisplayList:
        display_list: DisplayList = []
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        inside_body = False
        for token in tokens:
            if isinstance(token, Text) and (
                inside_body or self._check_is_view_source()
            ):
                for word in split_words_with_indentation(token.text):
                    cursor_x, cursor_y = self._layout_text(
                        word, cursor_x, cursor_y, self.font, display_list
                    )
            elif isinstance(token, Tag):
                if "body" in token.tag:
                    inside_body = True
                elif "/body" in token.tag:
                    inside_body = False
                self._tag_style(token)
        return display_list

    def resize(self, height: int, width: int):
        self.window_height = height
        self.window_width = width
        self.draw()

    def _layout_text(
        self,
        word: str,
        cursor_x: int,
        cursor_y: int,
        font: tkinter.font.Font,
        display_list: DisplayList,
    ) -> Tuple[int, int]:
        # Only newlines
        if is_only_newlines(word):
            cursor_y += int(self.VSTEP * 1.25) * count_newlines(word)
            cursor_x = self.HSTEP
            return cursor_x, cursor_y

        word_size = self.font.measure(word)

        # Line wrap
        if cursor_x + word_size > self.window_width - self.HSTEP:
            cursor_y += int(self.VSTEP * 1.25)
            cursor_x = self.HSTEP

        for c in word:
            letter_size = self.font.measure(c)
            if c == "\n":
                cursor_y += int(self.VSTEP * 1.25)
                cursor_x = self.HSTEP
                continue
            cursor_x += letter_size
            display_list.append((c, cursor_x, cursor_y, font))

        cursor_x += self.font.measure(" ")
        display_list.append((" ", cursor_x, cursor_y, font))
        return cursor_x, cursor_y

    def _tag_style(self, tag: Tag):
        if tag.tag == "i":
            self.style = "italic"
        elif tag.tag == "/i":
            self.style = "roman"
        elif tag.tag == "b":
            self.weight = "bold"
        elif tag.tag == "/b":
            self.weight = "normal"
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
