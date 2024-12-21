from dataclasses import dataclass
from cards.card import Card


@dataclass(frozen=True)
class MonsterCard(Card):
    attack: int
    defence: int
    level: int
