from enum import Enum
from invalid_target_error import InvalidTargetError
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
class Field:
    active_player: FieldHalf
    inactive_player: FieldHalf

    def game_start(deck_1, deck_2):
        _active_player = FieldHalf(deck_1)
        _inactive_player = FieldHalf(deck_2)

        _active_player = _active_player.draw(6)
        _inactive_player = _inactive_player.draw(5)

        return Field(_active_player, _inactive_player)

    def end_turn(self):
        field = self._flip_active_player()
        return field.draw()

    def _flip_active_player(self):
        return replace(
            self, active_player=self.inactive_player, inactive_player=self.active_player
        )

    def draw(self, count=1):
        return replace(self, active_player=self.active_player.draw(count))

    def play_from_hand(self, card_number):
        return self.active_player.play_from_hand(card_number)

    def attack(self, attacker_zone, target):
        if target == BattleTarget.Direct:
            return self._direct_attack(attacker_zone)
        else:
            return self._battle_monsters(attacker_zone, target)

    def _direct_attack(self, attacker_zone):
        if self.inactive_player.has_monsters():
            raise InvalidTargetError(
                "Cannot attack directly with monsters on the field"
            )
        attacker = self.active_player.monsterAt(attacker_zone)
        return attacker.target_directly()

    def _battle_monsters(self, attacker_zone, target):
        attacker = self.active_player.monsterAt(attacker_zone)
        defender = self.inactive_player.monsterAt(target)

        if defender is None or attacker is None:
            raise InvalidTargetError("No monster in defender zone")

        return attacker.target_monster(defender)
