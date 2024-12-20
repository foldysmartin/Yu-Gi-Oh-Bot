from dataclasses import dataclass

from card import Card
from effects import Destroy, LoseLifePoints, Summon


@dataclass(frozen=True)
class MonsterCard(Card):
    name: str
    attack: int
    defence: int
    level: int

    def play_from_hand(self):
        return Summon(self.instance_id)

    def target_monster(self, target):
        if self.attack < target.attack:
            return [
                Destroy(self.instance_id),
                LoseLifePoints(attacker=True, life_points=target.attack - self.attack),
            ]
        elif self.attack > target.attack:
            return [
                Destroy(target.instance_id),
                LoseLifePoints(attacker=False, life_points=self.attack - target.attack),
            ]
        else:
            return [Destroy(self.instance_id), Destroy(target.instance_id)]

    def target_directly(self):
        return [LoseLifePoints(attacker=False, life_points=self.attack)]
