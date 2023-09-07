from src.parser.data_parser import DataParser
from src.parser.file_parser import FileParser
from src.parser.html_parser import HTMLParser
from src.parser.parser import Parser
from src.utils.url import URL, AbstractURL, DataURL, FileURL


class ParserFactory:
    @staticmethod
    def create(url: AbstractURL) -> Parser:
        if isinstance(url, URL):
            return HTMLParser(url)
        elif isinstance(url, FileURL):
            return FileParser(url)
        elif isinstance(url, DataURL):
            return DataParser(url)
        raise ValueError(f"Unsupported URL type: {type(url)}")
