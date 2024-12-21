from dataclasses import dataclass, replace
from abstract.effect import Effect
from abstract_field import AbstractField
from cards.monster_card import MonsterCard
from game_state import GameState


@dataclass(frozen=True)
class Attack(Effect):
    attacker: MonsterCard

    def apply(self, field: AbstractField, game_state: GameState):
        return field, replace(
            game_state, previous_attacks=game_state.previous_attacks + [self.attacker]
        )
