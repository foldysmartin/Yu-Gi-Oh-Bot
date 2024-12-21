from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Dict, List

from cards.card import Card


# Todo move to a more appropriate file
class Zone(Enum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fith = 4


class NoMonsterError(Exception):
    pass


@dataclass(frozen=True)
class AbstractFieldHalf:
    deck: List[Card]
    hand: List[Card] = field(default_factory=list)
    monsters: Dict[Zone, Card] = field(default_factory=dict)

    def numberOfCards(self):
        return len(self.hand)

    def monster_count(self):
        return len(self.monsters)

    def destroy_monster(self, monster):
        monsters = {
            zone: card for zone, card in self.monsters.items() if card != monster
        }
        return replace(self, monsters=monsters)

    def summon_monster(self, card):
        free_zone = self._find_empty_zone()
        monsters = self.monsters | {free_zone: card}
        hand = [c for c in self.hand if c != card]
        return replace(self, monsters=monsters, hand=hand)

    def monsterAt(self, zone: Zone):
        if not zone in self.monsters:
            raise NoMonsterError(f"No monster in zone {zone}")
        return self.monsters[zone]

    def _find_empty_zone(self):
        for zone in Zone:
            if not zone in self.monsters:
                return zone
        raise NoMonsterError("No empty zone")


@dataclass(frozen=True)
class AbstractField:
    active_player: AbstractFieldHalf
    inactive_player: AbstractFieldHalf

    def summon_monster(self, card):
        return replace(self, active_player=self.active_player.summon_monster(card))

    def destroy_monster(self, monster):
        activated_player = self.active_player.destroy_monster(monster)
        inactivated_player = self.inactive_player.destroy_monster(monster)
        return replace(
            self, active_player=activated_player, inactive_player=inactivated_player
        )
