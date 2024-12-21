from dataclasses import dataclass

from abstract_field import AbstractField
from game_state import GameState


@dataclass(frozen=True)
class Action:
    def activate(self, field: AbstractField, game_state: GameState):
        raise NotImplementedError
