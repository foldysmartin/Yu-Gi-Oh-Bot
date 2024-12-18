from FieldHalf import FieldHalf


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

    def activate(self, card_number):
        return self.active_player.activate(card_number)

    def apply(
        self,
        effect,
    ):
        return replace(self, active_player=effect.apply(self.active_player))
