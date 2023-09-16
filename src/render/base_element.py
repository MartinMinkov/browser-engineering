from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BaseElement:
    parent: Optional[BaseElement] = None
    children: List[BaseElement] = field(default_factory=list)

    def __str__(self):
        return f"BaseElement({self.__class__.__name__})"
