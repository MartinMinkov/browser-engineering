from src.utils.url import URL, Scheme
from src.view.view import View


class FileView(View):
    def __init__(self, url: URL):
        if url.scheme != Scheme.File:
            raise ValueError("Unknown scheme {}".format(url.scheme))
        self.url = url

    def view_show(self, body: str):
        print(body)

    def view_load(self):
        with open(self.url.path, "r") as f:
            return f.read()
