from dataclasses import dataclass
from Player import Player
from abstract.effect import Effect
from abstract_field import AbstractField
from game_state import GameState


@dataclass(frozen=True)
class LoseLifePoints(Effect):
    amount: int
    player: Player

    def apply(self, field: AbstractField, game_state: GameState):
        return field, game_state.lose_life_points(self.player, self.amount)
