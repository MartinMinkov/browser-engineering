from src.utils.html import load
from src.utils.url import URL

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        url = URL(
            "file:///home/martin/Code/projects/python/browser-engineering/static/index.html"
        )
    else:
        url = URL(sys.argv[1])
    load(url)
