from src.utils.html import load
from src.utils.url import URL

if __name__ == "__main__":
    import sys

    url = URL(sys.argv[1])
    load(url)
