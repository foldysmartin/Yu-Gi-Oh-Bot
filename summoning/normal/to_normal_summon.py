from dataclasses import dataclass
from abstract.action import Action
from abstract_field import AbstractField
from cards.monster_card import MonsterCard
from game_state import GameState
from summoning.normal.normal_summon import NormalSummon


class SummoningError(Exception):
    pass


@dataclass(frozen=True)
class ToNormalSummon(Action):
    card: MonsterCard

    def activate(self, field: AbstractField, game_state: GameState):

        if field.active_player.monster_count() >= 5:
            raise SummoningError("Cannot summon more than 5 monsters")

        if game_state.normal_summoned:
            raise SummoningError("Already normal summoned this turn")

        return NormalSummon(self.card)
