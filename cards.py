import json

from monster_card import MonsterCard

with open('cards.json', 'r') as file:
    data = json.load(file)

def find_card(name):

    card = first(data, lambda card: card["name"] == name)

    return MonsterCard(name = card["name"], attack=card["attack"], defence=card["defence"], level=card["level"])

def first(iterable, condition = lambda x: True):
    return next(x for x in iterable if condition(x))