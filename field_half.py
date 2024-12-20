from enum import Enum
from abstract_field import AbstractFieldHalf, Zone
from monster_card import MonsterCard


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

    def play_from_hand(self, card_number):
        if len(self.hand) == 0:
            raise HandEmptyError("No cards to play")

        effect = self.hand[card_number - 1].play_from_hand()
        return effect

    def deck_size(self):
        return len(self.deck)

    def monsterAt(self, zone: Zone):
        return self.monsters[zone.value]
