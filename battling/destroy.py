from dataclasses import dataclass, replace
from Player import Player
from abstract.effect import Effect
from abstract_field import AbstractField
from cards.monster_card import MonsterCard
from game_state import GameState


@dataclass(frozen=True)
class Destroy(Effect):
    target: MonsterCard
    player: Player

    def apply(self, field: AbstractField, game_state: GameState):
        return field.destroy_monster(self.target), game_state
