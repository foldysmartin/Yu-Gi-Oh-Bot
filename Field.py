from invalid_target_error import InvalidTargetError
from field_half import FieldHalf


from dataclasses import dataclass, replace


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

    def battle(self, attacker_zone, defender_zone):
        attacker = self.active_player.monsterAt(attacker_zone)
        defender = self.inactive_player.monsterAt(defender_zone)

        if defender is None or attacker is None:
            raise InvalidTargetError("No monster in defender zone")

        return attacker.battle(defender)
