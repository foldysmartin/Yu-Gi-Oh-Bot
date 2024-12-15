from dataclasses import dataclass, field, replace
from enum import Enum
from typing import List

class Lost(Exception):
    pass

@dataclass(
           )
class Player:
    deck: List[int]
    _hand: List[int] = field(default_factory=list)


    def draw(self, count=1):
        if count > self.deck_size():
            raise Lost()

        return replace(self, _hand=self._hand+self.deck[0:count], deck = self.deck[count:])

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

    turn = 0
    player1: Player
    player2: Player

    active_player = 1
    phase: Phase

    def __str__(self):
        return f"""P1 Deck: {self.player1.deck_size()} Cards: {self.player1.numberOfCards()}
P2 Deck: {self.player2.deck_size()} Cards: {self.player2.numberOfCards()}"""
