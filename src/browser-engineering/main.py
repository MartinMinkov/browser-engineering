from src.utils.html import load
from src.utils.url import URLFactory

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        url = URLFactory.create(
            "file:///home/martin/Code/projects/python/browser-engineering/static/index.html"
        )
    else:
        url = URLFactory.create(sys.argv[1])
    load(url)
