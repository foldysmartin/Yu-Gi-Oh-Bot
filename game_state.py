@dataclass(frozen=True)
class GameState:
    normal_summoned = False

    def new_turn(self):
        return replace(self, normal_summoned=False)
