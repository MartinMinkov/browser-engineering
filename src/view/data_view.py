import base64
from urllib.parse import unquote

from src.utils.url import DataURL, Scheme
from src.view.view import View


class DataView(View):
    def __init__(self, url: DataURL):
        if url.scheme != Scheme.Data:
            raise ValueError("Unknown scheme {}".format(url.scheme))
        self.url = url

    def view_show(self, body: str):
        body_str = body
        if self.url.is_base64:
            body_bytes = body.encode("utf-8")
            body_str = base64.b64decode(body_bytes).decode("utf-8")
        print(unquote(body_str))

    def view_load(self):
        return self.url.data
