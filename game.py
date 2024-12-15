from dataclasses import dataclass, field, replace
from enum import Enum
from typing import List

from monster_card import MonsterCard

class Lost(Exception):
    pass

class Zone(Enum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fith = 4


@dataclass(
           )
class Player:
    deck: List[MonsterCard]
    _hand: List[MonsterCard] = field(default_factory=list)
    _monsters: List[MonsterCard] = field(default_factory=lambda: [None, None, None, None, None])



    def draw(self, count=1):
        if count > self.deck_size():
            raise Lost()

        return replace(self, _hand=self._hand+self.deck[0:count], deck = self.deck[count:])
    
    def activate(self, card_number, zone:Zone):
        card = self._hand[card_number - 1]
        monsters = self._monsters[:]
        monsters[zone.value] = card

        return replace(self, _hand= self._hand[:card_number - 1] + self._hand[card_number:], _monsters = monsters)
    
    def monsterAt(self, zone:Zone):
        return self._monsters[zone.value]

    def numberOfCards(self):
        return len(self._hand)
    
    def deck_size(self):
        return len(self.deck)
    
class Phase(Enum):
    Draw = 0

@dataclass()
class Game:
    def __init__(self, player1, player2):

        self.phase = Phase.Draw
        self.player1 = player1.draw(6)
        self.player2 = player2.draw(5)

    def end_turn(self):
        self.phase = Phase.Draw
        self.active_player = 2
        self.draw_phase()

    def draw_phase(self):
        if self.active_player == 1:
            self.player1 = self.player1.draw()
        else:
            self.player2 = self.player2.draw()

    def activate(self, card, zone):
        if self.active_player == 1:
            self.player1 = self.player1.activate(card, zone)
        else:
            self.player2 = self.player2.activate(card, zone)

    turn = 0
    player1: Player
    player2: Player

    active_player = 1
    phase: Phase

    def __str__(self):
        return f"""P1 Deck: {self.player1.deck_size()} Cards: {self.player1._hand}
Monsters {self.player1._monsters}
Monsters {self.player1._monsters}
P2 Deck: {self.player2.deck_size()} Cards: {self.player2._hand}"""
