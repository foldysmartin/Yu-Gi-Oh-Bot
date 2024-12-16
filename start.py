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


game = Game.start(create_deck(), create_deck())

root = Tk()
root.geometry("600x400+50+50")
root.resizable(0, 0)


for i, card in enumerate(game.field.active_player._hand):
    label = Label(root, text=card.name)
    label.grid(row=1, column=i)

for i, card in enumerate(game.field.inactive_player._hand):
    label = Label(root, text="Hidden")
    label.grid(row=0, column=i)

root.mainloop()
