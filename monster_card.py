from dataclasses import dataclass
from uuid import UUID

from card import Card
from effects import Destroy, Summon


@dataclass(frozen=True)
class MonsterCard(Card):
    name: str
    attack: int
    defence: int
    level: int

    def play_from_hand(self):
        return Summon(self.instance_id)

    def battle(self, target):
        if self.attack < target.attack:
            return [Destroy(self.instance_id)]
        elif self.attack > target.attack:
            return [Destroy(target.instance_id)]
        else:
            return [Destroy(self.instance_id), Destroy(target.instance_id)]
