from src.utils.headers import Headers


class Response:
    def __init__(
        self, status_code: int, reason_phrase: str, headers: Headers, body: str
    ):
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers
        self.body = body

    def is_successful(self):
        return 200 <= self.status_code < 300

    def __str__(self):
        # Convert the response to a string representation
        return f"{self.status_code} {self.reason_phrase} {self.headers} {self.body}"
