from dataclasses import dataclass
from abstract_field import AbstractField
from game_state import GameState


@dataclass(frozen=True)
class Effect:
    def apply(self, field: AbstractField, game_state: GameState):
        raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, Effects):
            return Effects([self] + other.effects)
        elif isinstance(other, Effect):
            return Effects([self, other])
        else:
            raise ValueError(f"Cannot add {other} to Effect")


@dataclass(frozen=True)
class Effects:
    effects: list[Effect]

    def apply(self, field: AbstractField, game_state: GameState):
        for effect in self.effects:
            field, game_state = effect.apply(field, game_state)
        return field, game_state

    def __add__(self, other):
        if isinstance(other, Effects):
            return Effects(self.effects + other.effects)
        elif isinstance(other, Effect):
            return Effects(self.effects + [other])
        else:
            raise ValueError(f"Cannot add {other} to Effects")
