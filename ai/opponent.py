import random

from game import Game


class Opponent:
    def __init__(self, player):
        self.player = player

    def play(self, game: Game):
        return list(self._play(game))

    def _play(self, game: Game):
        while game.game_state.active_player == self.player and game.still_playing():
            action = random.choice(game.avaliable_actions())
            yield game.trigger_action(action)
