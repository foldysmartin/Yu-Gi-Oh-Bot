from dataclasses import dataclass, replace
from abstract.effect import Effect
from abstract_field import AbstractField
from cards.monster_card import MonsterCard
from game_state import GameState


@dataclass(frozen=True)
class NormalSummon(Effect):
    card: MonsterCard

    def apply(self, field: AbstractField, game_state: GameState):

        field = field.summon_monster(self.card)
        game_state = replace(game_state, normal_summoned=True)
        return field, game_state
