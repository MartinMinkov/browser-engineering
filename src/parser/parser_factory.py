from src.parser.data_parser import DataParser
from src.parser.file_parser import FileParser
from src.parser.html_parser import HTMLParser
from src.parser.parser import Parser
from src.resolver.data_resolver import DataResolver
from src.resolver.file_resolver import FileResolver
from src.resolver.http_resolver import HTTPResolver
from src.resolver.resolver import Resolver


class ParserFactory:
    @staticmethod
    def create(resolver: Resolver) -> Parser:
        if isinstance(resolver, HTTPResolver):
            return HTMLParser(resolver)
        elif isinstance(resolver, FileResolver):
            return FileParser(resolver)
        elif isinstance(resolver, DataResolver):
            return DataParser(resolver)
        raise ValueError(f"Unsupported resolver type: {type(resolver)}")
