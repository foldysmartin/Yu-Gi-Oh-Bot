from game import Game, Player


player = Player(deck = [1,1,1,1,1,1])
game = Game(player, player)

print(game)

while True:

    action = input("e for endturn\n")

    if action == "e":
        game.end_turn()

    print(game)