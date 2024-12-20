from dataclasses import dataclass, field, replace

from Player import Player


@dataclass(frozen=True)
class GameState:
    normal_summoned: bool = False
    active_player: Player = Player.One

    @property
    def inactive_player(self):
        return Player.Two if self.active_player == Player.One else Player.One

    _life_points: list[int] = field(default_factory=lambda: [8000, 8000])

    def end_turn(self):
        active_player = Player.Two if self.active_player == Player.One else Player.One
        return replace(self, normal_summoned=False, active_player=active_player)

    def life_points(self, player):
        return self._life_points[player.value]

    def lose_life_points(self, player, amount):
        life_points = self._life_points[:]
        life_points[player.value] -= amount
        return replace(self, _life_points=life_points)
