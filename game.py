from dataclasses import dataclass, field, replace
from enum import Enum
from typing import List

from monster_card import MonsterCard


class OutOfCards(Exception):
    pass


class SummoningError(Exception):
    pass


class Zone(Enum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fith = 4


@dataclass(frozen=True)
class FieldHalf:
    deck: List[MonsterCard]
    hand: List[MonsterCard] = field(default_factory=list)
    monsters: List[MonsterCard] = field(
        default_factory=lambda: [
            None,
            None,
            None,
            None,
            None,
        ]  # Should maybe be an empty slot type
    )

    def draw(self, count=1):
        if count > self.deck_size():
            raise OutOfCards()

        return replace(
            self, hand=self.hand + self.deck[0:count], deck=self.deck[count:]
        )

    def activate(self, card_number):
        if self.numberOfCards() == 0:
            raise SummoningError("No cards to summon")

        zone = first_index(self.monsters, lambda monster: monster == None)
        if zone == None:
            raise SummoningError("No empty zones to summon to")

        card = self.hand[card_number - 1]
        monsters = self.monsters[:]
        monsters[zone] = card

        return replace(
            self,
            hand=self.hand[: card_number - 1] + self.hand[card_number:],
            monsters=monsters,
        )

    def deck_size(self):
        return len(self.deck)

    def monsterAt(self, zone: Zone):
        return self.monsters[zone.value]

    def numberOfCards(self):
        return len(self.hand)


def first_index(iterable, condition=lambda x: True):
    return next((i for i, x in enumerate(iterable) if condition(x)), None)


class Player(Enum):
    One = 1
    Two = 2


@dataclass(frozen=True)
class Field:
    active_player: FieldHalf
    inactive_player: FieldHalf

    def game_start(deck_1, deck_2):
        _active_player = FieldHalf(deck_1)
        _inactive_player = FieldHalf(deck_2)

        _active_player = _active_player.draw(6)
        _inactive_player = _inactive_player.draw(5)

        return Field(_active_player, _inactive_player)

    def end_turn(self):
        field = self._flip_active_player()
        return field.draw()

    def _flip_active_player(self):
        return replace(
            self, active_player=self.inactive_player, inactive_player=self.active_player
        )

    def draw(self, count=1):
        return replace(self, active_player=self.active_player.draw(count))

    def activate(self, card_number):
        return replace(self, active_player=self.active_player.activate(card_number))


class Phase(Enum):
    Draw = 0


@dataclass()
class Game:

    turn = 0
    field: Field
    phase: Phase
    current_player: Player = Player.One

    def __init__(self, field):

        self.phase = Phase.Draw
        self.field = field

    def start(deck_1, deck_2):
        field = Field.game_start(deck_1, deck_2)
        return Game(field)

    def end_turn(self):
        self.phase = Phase.Draw
        self.field = self.field.end_turn()
        self.current_player = (
            Player.Two if self.current_player == Player.One else Player.One
        )

    def activate(self, card):
        self.field = self.field.activate(card)

    def fetch_hand(self, player):
        return self._fetch_field(player).hand

    def fetch_monsters(self, player):
        return self._fetch_field(player).monsters

    def _fetch_field(self, player):
        return (
            self.field.active_player
            if player == self.current_player
            else self.field.inactive_player
        )
