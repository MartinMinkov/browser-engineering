from src.networking.headers import Headers


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

    def __eq__(self, other):
        return (
            self.status_code == other.status_code
            and self.reason_phrase == other.reason_phrase
            and self.headers == other.headers
            and self.body == other.body
        )

    def __str__(self):
        # Convert the response to a string representation
        return f"{self.status_code} {self.reason_phrase} {self.headers} {self.body}"
