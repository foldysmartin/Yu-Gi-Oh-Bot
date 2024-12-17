from dataclasses import dataclass
from enum import Enum

from Field import Field


class Player(Enum):
    One = 1
    Two = 2


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
