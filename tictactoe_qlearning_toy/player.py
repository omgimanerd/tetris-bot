"""
The Player class and its subclasses encapsulate logic for playing a game of
tic tac toe.
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods

import random

import numpy as np

from tictactoe_qlearning_toy.board import Board

class Player():
    def __init__(self, marker):
        assert marker in 'XO'
        self.marker = marker

    def play(self, board):
        raise NotImplementedError('play() not overriden!')

class RandomPlayer():
    def play(self, board):
        return random.choice(np.argwhere(board.board == 0))

class MinMaxPlayer(Player):
    def __init__(self, marker):
        super().__init__(marker)

    def play(self, board):
        pass

if __name__ == '__main__':
    b = Board([
        [0, 2, 0],
        [1, 1, 1],
        [0, 0, 2],
    ])
    p = RandomPlayer()
    print(p.play(b))
