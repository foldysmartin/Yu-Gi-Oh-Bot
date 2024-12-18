from dataclasses import dataclass
from card import Card


@dataclass(frozen=True)
class EmptySpace(Card):
    def __init__(self):
        super().__init__(None)
