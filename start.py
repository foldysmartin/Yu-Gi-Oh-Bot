from tkinter import Label, Tk
from cards import find_card
from game import Game, Zone


def create_deck():
    return [
        find_card("Mystical Elf"),
        find_card("Mystical Elf"),
        find_card("Mystical Elf"),
        find_card("Mystical Elf"),
        find_card("Mystical Elf"),
        find_card("Mystical Elf"),
    ]


class GameWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry("600x400+50+50")
        self.resizable(0, 0)

        self.cards = []
        self.game = Game.start(create_deck(), create_deck())

        self._redraw()

    def _redraw(self):
        for card in self.cards:
            card.destroy()
        self.cards = []
        self._draw_opponent_hand()
        self._draw_player_hand()
        self._draw_monster_zone()

    def _draw_player_hand(
        self,
    ):
        for i, card in enumerate(self.game.field.active_player._hand):
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
        for i, card in enumerate(self.game.field.inactive_player._hand):
            label = Label(self, text="Hidden")
            label.grid(row=0, column=i)
            self.cards.append(label)

    def _draw_monster_zone(self):
        for i, card in enumerate(self.game.field.active_player._monsters):
            card_text = card.name if card else "Empty"
            label = Label(self, text=card_text)
            label.grid(row=3, column=i)
            self.cards.append(label)

    def _card_in_hand_lambda(self, card_number):
        return lambda e: self._card_in_hand(card_number)

    def _card_in_hand(self, card_number):
        print(card_number)
        self.game.activate(card_number)
        self._redraw()


window = GameWindow()
window.mainloop()
