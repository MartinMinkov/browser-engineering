import tkinter

from src.render.browser import Browser
from src.utils.url_factory import URLFactory

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1 or sys.argv[1] == "":
        url = URLFactory.create(
            "file:///home/martin/Code/projects/python/browser-engineering/static/index.html"
        )
    else:
        url = URLFactory.create(sys.argv[1])
    Browser().load(url)
    tkinter.mainloop()
