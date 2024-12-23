import numpy as np

class WinBuffer:
    def __init__(self, size):
        self.size = size
        self.data = np.zeros(size, dtype=float)
        self.index = 0
        self.is_full = False

    def win(self):
        self._append(1)

    def lose(self):
        self._append(-1)

    def _append(self, value):
        self.data[self.index] = value
        self.index = (self.index + 1) % self.size
        if self.index == 0:
            self.is_full = True

    def win_percentage(self):
        wins = np.count_nonzero(self.data == 1)
        loses = np.count_nonzero(self.data == -1)
        return wins / (wins + loses) if wins > 0 else 0

