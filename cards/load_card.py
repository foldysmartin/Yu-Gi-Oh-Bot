import json
from uuid import uuid4

from cards.card import Card
from cards.monster_card import MonsterCard
from summoning.normal.to_normal_summon import ToNormalSummon


with open("cards.json", "r") as file:
    data = json.load(file)


def find_card(name) -> Card:

    card = first(data, lambda card: card["name"] == name)

    return MonsterCard(
        instance_id=uuid4(),
        name=card["name"],
        attack=card["attack"],
        defence=card["defence"],
        level=card["level"],
        activator=ToNormalSummon,
    )


def first(iterable, condition=lambda x: True):
    return next(x for x in iterable if condition(x))
