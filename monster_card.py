from dataclasses import dataclass
from uuid import UUID

from card import Card
from effects import Summon


@dataclass
class MonsterCard(Card):
    name: str
    attack: int
    defence: int
    level: int

    def activate(self):
        return Summon(self.instance_id)
