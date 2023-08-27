from src.utils.headers import Headers


class Request:
    def __init__(self, path: str, method: str = "GET", headers: Headers = None):
        self.headers = headers
        self.path = path
        self.method = method

    def __str__(self):
        return "{} {} HTTP/1.0\r\n{}\r\n\r\n".format(
            self.method, self.path, self.headers
        )
