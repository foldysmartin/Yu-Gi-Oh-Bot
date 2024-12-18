from dataclasses import dataclass, field
from typing import List

from card import Card


@dataclass(frozen=True)
class AbstractFieldHalf:
    deck: List[Card]
    hand: List[Card] = field(default_factory=list)
    monsters: List[Card] = field(
        default_factory=lambda: [
            None,
            None,
            None,
            None,
            None,
        ]  # Should maybe be an empty slot type
    )

    def numberOfCards(self):
        return len(self.hand)


@dataclass(frozen=True)
class AbstractField:
    active_player: AbstractFieldHalf
    inactive_player: AbstractFieldHalf
