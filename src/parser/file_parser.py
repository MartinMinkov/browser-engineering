from src.parser.parser import Parser
from src.resolver.file_resolver import FileResolver


class FileParser(Parser):
    resolver: FileResolver

    def __init__(self, resolver: FileResolver):
        self.resolver = resolver

    def lex(self) -> str:
        return self.resolver.resolve()
