from dataclasses import dataclass, field, replace
from enum import Enum
from typing import List

from card import Card
from empty_space import EmptySpace


# Todo move to a more appropriate file
class Zone(Enum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fith = 4


@dataclass(frozen=True)
class AbstractFieldHalf:
    deck: List[Card]
    hand: List[Card] = field(default_factory=list)
    monsters: List[Card] = field(
        default_factory=lambda: [
            EmptySpace(),
            EmptySpace(),
            EmptySpace(),
            EmptySpace(),
            EmptySpace(),
        ]  # Should maybe be an empty slot type
    )

    def numberOfCards(self):
        return len(self.hand)

    def destroy_monster(self, index):
        return replace(
            self,
            monsters=self.monsters[:index]
            + [EmptySpace()]
            + self.monsters[index + 1 :],
        )


@dataclass(frozen=True)
class AbstractField:
    active_player: AbstractFieldHalf
    inactive_player: AbstractFieldHalf
