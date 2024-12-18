from dataclasses import dataclass
from enum import Enum

from Field import Field
from game_state import GameState


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
    game_state: GameState = GameState()

    def __init__(self, field):

        self.phase = Phase.Draw
        self.field = field

    def start(deck_1, deck_2):
        field = Field.game_start(deck_1, deck_2)
        return Game(field)

    def end_turn(self):
        self.phase = Phase.Draw
        self.field = self.field.end_turn()
        self.game_state = self.game_state.end_turn()
        self.current_player = (
            Player.Two if self.current_player == Player.One else Player.One
        )

    def activate(self, card):
        effect = self.field.activate(card)
        self.game_state, self.field = effect.apply(self.game_state, self.field)

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
