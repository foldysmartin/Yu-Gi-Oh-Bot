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
    _deck: List[MonsterCard]
    _hand: List[MonsterCard] = field(default_factory=list)
    _monsters: List[MonsterCard] = field(
        default_factory=lambda: [None, None, None, None, None]
    )

    def draw(self, count=1):
        if count > self.deck_size():
            raise OutOfCards()

        return replace(
            self, _hand=self._hand + self._deck[0:count], _deck=self._deck[count:]
        )

    def activate(self, card_number):

        zone = first_index(self._monsters, lambda monster: monster == None)
        if zone == None:
            raise SummoningError("No empty zones to summon to")

        card = self._hand[card_number - 1]
        monsters = self._monsters[:]
        monsters[zone] = card

        return replace(
            self,
            _hand=self._hand[: card_number - 1] + self._hand[card_number:],
            _monsters=monsters,
        )

    def monsterAt(self, zone: Zone):
        return self._monsters[zone.value]

    def numberOfCards(self):
        return len(self._hand)

    def deck_size(self):
        return len(self._deck)


def first_index(iterable, condition=lambda x: True):
    return next((i for i, x in enumerate(iterable) if condition(x)), None)


class Player(Enum):
    One = 1
    Two = 2


@dataclass(frozen=True)
class Field:
    active_player: FieldHalf
    inactive_player: FieldHalf

    current_player: Player = Player.One

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
            self,
            active_player=self.inactive_player,
            inactive_player=self.active_player,
            current_player=(
                Player.Two if self.current_player == Player.One else Player.One
            ),
        )

    def draw(self, count=1):
        return replace(self, active_player=self.active_player.draw(count))

    def activate(self, card_number, zone: Zone):
        return replace(
            self, active_player=self.active_player.activate(card_number, zone)
        )


class Phase(Enum):
    Draw = 0


@dataclass()
class Game:
    def __init__(self, field):

        self.phase = Phase.Draw
        self.field = field

    def start(deck_1, deck_2):
        field = Field.game_start(deck_1, deck_2)
        return Game(field)

    def end_turn(self):
        self.phase = Phase.Draw
        self.field = self.field.end_turn()

    def activate(self, card, zone):
        self.field = self.field.activate(card, zone)

    turn = 0
    field: Field
    phase: Phase

    def __str__(self):
        return f"""Active Deck: {self.field.active_player.deck_size()} Cards: {self.field.active_player._hand}
Monsters {self.field.active_player._monsters}
Monsters {self.field.inactive_player._monsters}
Inactive Deck: {self.field.inactive_player.deck_size()} Cards: {self.field.inactive_player._hand}"""
