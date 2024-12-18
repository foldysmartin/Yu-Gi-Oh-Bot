from dataclasses import dataclass, replace
from uuid import UUID
from abstract_field import AbstractField
from game_state import GameState


class Effect:
    def apply(self, game_state: GameState, field: AbstractField):
        raise NotImplementedError


class SummoningError(Exception):
    pass


@dataclass(frozen=True)
class Summon(Effect):
    instance_id: UUID

    def apply(self, game_state: GameState, field: AbstractField):
        active_player = field.active_player
        if active_player.numberOfCards() == 0:
            raise SummoningError("No cards to summon")

        if game_state.normal_summoned:
            raise SummoningError("Already normal summoned this turn")

        zone = first_index(active_player.monsters, lambda monster: monster == None)
        if zone == None:
            raise SummoningError("No empty zones to summon to")

        card_index = first_index(
            active_player.hand, lambda card: card.instance_id == self.instance_id
        )

        if card_index is None:
            raise SummoningError("Card not found in hand")

        monsters = active_player.monsters[:]
        monsters[zone] = active_player.hand[card_index]

        active_player = replace(
            active_player,
            hand=active_player.hand[:card_index] + active_player.hand[card_index + 1 :],
            monsters=monsters,
        )

        return replace(game_state, normal_summoned=True), replace(
            field,
            active_player=active_player,
        )


def first_index(iterable, condition=lambda x: True):
    return next((i for i, x in enumerate(iterable) if condition(x)), None)


def first(iterable, condition=lambda x: True):
    return next(x for x in iterable if condition(x))
