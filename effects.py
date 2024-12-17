from dataclasses import dataclass, replace
from uuid import UUID
from abstract_field import AbstractField


class Effect:
    def apply(self, player_field: AbstractField):
        raise NotImplementedError


class SummoningError(Exception):
    pass


@dataclass(frozen=True)
class Summon(Effect):
    instance_id: UUID

    def apply(self, player_field: AbstractField):
        if player_field.numberOfCards() == 0:
            raise SummoningError("No cards to summon")

        zone = first_index(player_field.monsters, lambda monster: monster == None)
        if zone == None:
            raise SummoningError("No empty zones to summon to")

        card_index = first_index(
            player_field.hand, lambda card: card.instance_id == self.instance_id
        )

        if card_index is None:
            raise SummoningError("Card not found in hand")

        monsters = player_field.monsters[:]
        monsters[zone] = player_field.hand[card_index]

        return replace(
            player_field,
            hand=player_field.hand[:card_index] + player_field.hand[card_index + 1 :],
            monsters=monsters,
        )


def first_index(iterable, condition=lambda x: True):
    return next((i for i, x in enumerate(iterable) if condition(x)), None)


def first(iterable, condition=lambda x: True):
    return next(x for x in iterable if condition(x))
