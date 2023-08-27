class Headers:
    def __init__(self):
        self.headers = {}
        self.encoding = "utf8"

    def add_header(self, header: str, value: str):
        self.headers[header.lower()] = value.strip()

    def remove_header(self, header: str):
        del self.headers[header.lower()]

    def get_header(self, header: str) -> str:
        return self.headers[header.lower()]

    def set_encoding(self, encoding: str):
        self.encoding = encoding

    def __str__(self) -> str:
        string = ""
        for header, value in self.headers.items():
            string += header + ": " + value + "\r\n"
            return string

    def print_headers(self):
        for header, value in self.headers.items():
            print(header + ": " + value)

    def default(host: str):
        headers = Headers()
        headers.add_header("host", host)
        headers.add_header("user-agent", "browser-engineering")
        headers.add_header("connection", "close")
        headers.add_header("accept", "*/*")
        headers.add_header("accept-encoding", "gzip")
        return headers
