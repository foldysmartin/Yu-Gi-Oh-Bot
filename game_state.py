from dataclasses import dataclass, replace


@dataclass(frozen=True)
class GameState:
    normal_summoned: bool = False

    def new_turn(self):
        return replace(self, normal_summoned=False)
