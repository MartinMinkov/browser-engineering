from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Attributes:
    attributes: Dict[str, str]

    @staticmethod
    def from_tag(tag_parts: List[str]) -> Attributes:
        attributes = Attributes({})
        for attr_pair in tag_parts:
            if "=" in attr_pair:
                key, value = attr_pair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", '"']:
                    value = value[1:-1]
                attributes.set_attribute(key, value)
            else:
                attributes.set_attribute(attr_pair, "")
        return attributes

    def get_attribute(self, key: str) -> str:
        return self.attributes.get(key, "")

    def set_attribute(self, key: str, value: str):
        self.attributes[key.lower()] = value

    def __str__(self) -> str:
        return " ".join([f'{key}="{value}"' for key, value in self.attributes.items()])

    def size(self) -> int:
        return len(self.attributes)
