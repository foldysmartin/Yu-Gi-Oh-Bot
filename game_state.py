from dataclasses import dataclass, field, replace
from enum import Enum

from Player import Player


class Phase(Enum):
    Draw = 0
    Main1 = 1
    Battle = 2
    Main2 = 3
    End = 4


@dataclass(frozen=True)
class GameState:
    normal_summoned: bool = False
    active_player: Player = Player.One
    phase: Phase = Phase.Main1

    @property
    def inactive_player(self):
        return Player.Two if self.active_player == Player.One else Player.One

    _life_points: list[int] = field(default_factory=lambda: [8000, 8000])

    def can_normal_summon(self):
        return not self.normal_summoned and (
            self.phase == Phase.Main1 or self.phase == Phase.Main2
        )

    def _next_phase(self):
        if self.phase == Phase.Draw:
            return Phase.Main1
        elif self.phase == Phase.Main1:
            return Phase.Battle
        elif self.phase == Phase.Battle:
            return Phase.Main2
        else:
            return Phase.End

    def change_phase(self):
        next_phase = self._next_phase()
        if next_phase == Phase.End:
            return self.end_turn()
        else:
            return replace(self, phase=next_phase)

    def end_turn(self):
        active_player = Player.Two if self.active_player == Player.One else Player.One
        return replace(
            self, normal_summoned=False, active_player=active_player, phase=Phase.Draw
        )

    def life_points(self, player):
        return self._life_points[player.value]

    def lose_life_points(self, player, amount):
        life_points = self._life_points[:]
        life_points[player.value] -= amount
        return replace(self, _life_points=life_points)
