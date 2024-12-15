from cards import find_card
from game import Game, Zone


monster = find_card("Mystical Elf")
deck = [monster,monster,monster,monster,monster,monster]
game = Game(deck, deck)

print(game)

while True:

    action = input("e for endturn, a for activate \n")

    if action == "e":
        game.end_turn()
    elif action == "a":
        card = int(input("Enter card number\n"))
        zone = int(input("Enter zone number\n")) - 1

        game.activate(card, Zone(zone))

    print(game)