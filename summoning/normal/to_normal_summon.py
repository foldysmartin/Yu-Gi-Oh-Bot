from dataclasses import dataclass
from abstract.action import Action
from abstract_field import AbstractField
from cards.monster_card import MonsterCard
from game_state import GameState, Phase
from summoning.normal.normal_summon import NormalSummon


class SummoningError(Exception):
    pass


@dataclass(frozen=True)
class ToNormalSummon(Action):
    index: int

    def activate(self, field: AbstractField, game_state: GameState):

        if field.active_player.monster_count() >= 5:
            raise SummoningError("Cannot summon more than 5 monsters")

        if game_state.normal_summoned:
            raise SummoningError("Already normal summoned this turn")

        if not game_state.phase is Phase.Main1 and not game_state.phase is Phase.Main2:
            raise SummoningError("Can only normal summon in main phases")
        
        if self.index >= len(field.active_player.hand):
            raise SummoningError("Invalid hand index")
        
        card = field.active_player.hand[self.index]

        return NormalSummon(card)
