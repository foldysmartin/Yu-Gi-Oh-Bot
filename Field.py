from enum import Enum
from abstract_field import AbstractField
from battling.to_battle import ToBattle
from field_half import FieldHalf


from dataclasses import dataclass, replace


class BattleTarget(Enum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fith = 4
    Direct = 5


@dataclass(frozen=True)
class Field(AbstractField):
    active_player: FieldHalf
    inactive_player: FieldHalf

    def game_start(deck_1, deck_2):
        _active_player = FieldHalf(deck_1)
        _inactive_player = FieldHalf(deck_2)

        _active_player = _active_player.draw(6)
        _inactive_player = _inactive_player.draw(5)

        return Field(_active_player, _inactive_player)

    def end_turn(self):
        field = self
        if field.active_player.numberOfCards() > 7:
            discard = field.active_player.hand[0]
            field = replace(field, active_player=field.active_player.discard(discard))
        field = field._flip_active_player()
        return field.draw()

    def _flip_active_player(self):
        return replace(
            self, active_player=self.inactive_player, inactive_player=self.active_player
        )

    def draw(self, count=1):
        return replace(self, active_player=self.active_player.draw(count))

    def attack(self, attacker_zone, target):
        return ToBattle(attacker_zone, target)
