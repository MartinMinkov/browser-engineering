from src.parser.parser import Parser
from src.resolver.data_resolver import DataResolver


class DataParser(Parser):
    resolver: DataResolver

    def __init__(self, resolver: DataResolver):
        self.resolver = resolver

    def lex(self) -> str:
        return self.resolver.resolve()
