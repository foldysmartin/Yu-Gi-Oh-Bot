from game import Game, Player


player = Player(deck = [1,1,1,1,1,1])
game = Game(player, player)

print(game)

action = input("e for endturn")
print(action)

if action == "e":
    game.end_turn()

print(game)