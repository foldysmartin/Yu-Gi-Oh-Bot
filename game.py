from dataclasses import dataclass
from enum import Enum

from Field import Field
from Player import Player
from game_state import GameState, Phase


@dataclass()
class Game:

    turn = 0
    field: Field
    game_state: GameState = GameState()

    def __init__(self, field):
        self.phase = Phase.Draw
        self.field = field

    def start(deck_1, deck_2):
        field = Field.game_start(deck_1, deck_2)
        return Game(field)

    def next_phase(self):
        self.game_state = self.game_state.change_phase()
        if self.game_state.phase == Phase.Draw:
            self.field = self.field.end_turn()
            self.game_state = self.game_state.change_phase()

    def play_from_hand(self, card):
        effect = self.field.play_from_hand(card)
        self.game_state, self.field = effect.apply(self.game_state, self.field)

    def battle(self, attacker_zone, target):
        effects = self.field.attack(attacker_zone, target)

        for effect in effects:
            self.game_state, self.field = effect.apply(self.game_state, self.field)

    def fetch_hand(self, player):
        return self._fetch_field(player).hand

    def fetch_monsters(self, player):
        return self._fetch_field(player).monsters

    def _fetch_field(self, player):
        return (
            self.field.active_player
            if player == self.game_state.active_player
            else self.field.inactive_player
        )
