from tkinter import Button, Label, Tk
from abstract_field import Zone
from cards import find_card
from empty_space import EmptySpace
from game import Game, Player


def create_deck():
    return [
        find_card("Mystical Elf"),
        find_card("Feral Imp"),
        find_card("Winged Dragon, Guardian of the Fortress #1"),
        find_card("Beaver Warrior"),
        find_card("Celtic Guardian"),
        find_card("Mammoth Graveyard"),
        find_card("Great White"),
        find_card("Silver Fang"),
        find_card("Giant Soldier of Stone"),
        find_card("Dragon Zombie"),
        find_card("Witty Phantom"),
        find_card("Claw Reacher"),
        find_card("Mystic Clown"),
        find_card("Ancient Elf"),
        find_card("Magical Ghost"),
        find_card("Neo the Magic Swordsman"),
        find_card("Baron of the Fiend Sword"),
        find_card("Man-Eating Treasure Chest"),
        find_card("Sorcerer of the Doomed"),
    ]


class BadBot:
    def __init__(self, game):
        self.game = game

    def play(self):
        try:
            self.game.play_from_hand(1)
        except:
            pass
        self.game.end_turn()


class GameWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry("600x400+50+50")
        self.resizable(0, 0)
        self.cards = []
        self.game = Game.start(create_deck(), create_deck())

        self._redraw()
        self._draw_end_turn_button()

    def _redraw(self):
        for card in self.cards:
            card.destroy()
        self.cards = []
        self.selected = None
        self._draw_opponent_hand()
        self._draw_player_hand()
        self._draw_player_monster_zone()
        self._draw_opponent_monster_zone()

    def _draw_player_hand(
        self,
    ):
        for i, card in enumerate(self.game.fetch_hand(Player.One)):
            label = Label(self, text=card.name)
            label.grid(row=4, column=i)

            card_number = i + 1
            label.bind(
                "<Button-1>",
                self._card_in_hand_lambda(card_number),
            )
            self.cards.append(label)

    def _draw_opponent_hand(
        self,
    ):
        for i, card in enumerate(self.game.fetch_hand(Player.Two)):
            label = Label(self, text="Hidden")
            label.grid(row=0, column=i)
            self.cards.append(label)

    def _draw_player_monster_zone(self):
        for i, card in enumerate(self.game.fetch_monsters(Player.One)):
            card_text = card.name if type(card) is not EmptySpace else "Empty"
            label = Label(self, text=card_text)
            label.grid(row=3, column=i)
            label.bind("<Button-1>", self._select_lambda(Zone(i)))
            self.cards.append(label)

    def _draw_opponent_monster_zone(self):
        for i, card in enumerate(self.game.fetch_monsters(Player.Two)):
            card_text = card.name if type(card) is not EmptySpace else "Empty"
            label = Label(self, text=card_text)
            label.grid(row=1, column=i)
            label.bind("<Button-1>", self._attack_lambda(Zone(i)))
            self.cards.append(label)

    def _draw_end_turn_button(self):
        button = Button(self, text="End Turn", command=self._end_turn)
        button.grid(row=5, column=0, columnspan=6)

    def _card_in_hand_lambda(self, card_number):
        return lambda e: self._card_in_hand(card_number)

    def _card_in_hand(self, card_number):
        self.game.play_from_hand(card_number)
        self._redraw()

    def _select_lambda(self, zone):
        return lambda event: self._select(event.widget, zone)

    def _select(self, widget, zone):
        widget.config(bg="red")
        self.selected = zone

    def _attack_lambda(self, zone):
        return lambda event: self._attack(zone)

    def _attack(self, zone):
        if self.selected:
            self.game.battle(self.selected, zone)
            self._redraw()

    def _end_turn(self):
        self.game.end_turn()

        BadBot(self.game).play()
        self._redraw()


window = GameWindow()
window.mainloop()
