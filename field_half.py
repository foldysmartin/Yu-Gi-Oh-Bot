from enum import Enum
from abstract_field import AbstractFieldHalf, Zone


class OutOfCards(Exception):
    pass


from dataclasses import dataclass, field, replace
from typing import List


class HandEmptyError(Exception):
    pass


@dataclass(frozen=True)
class FieldHalf(AbstractFieldHalf):
    def draw(self, count=1):
        if count > self.deck_size():
            raise OutOfCards()

        return replace(
            self, hand=self.hand + self.deck[0:count], deck=self.deck[count:]
        )

    def deck_size(self):
        return len(self.deck)

    def discard(self, card):
        return replace(self, hand=[c for c in self.hand if c != card])
