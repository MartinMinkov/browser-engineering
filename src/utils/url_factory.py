from src.utils.url import URL, AbstractURL, DataURL, FileURL, Scheme


class URLFactory:
    @staticmethod
    def create(url: str) -> AbstractURL:
        if url.startswith(str(Scheme.Data)):
            return DataURL(url)
        elif url.startswith(str(Scheme.File)):
            return FileURL(url)
        else:
            return URL(url)
