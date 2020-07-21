"""
The Player class and its subclasses encapsulate logic for playing a game of
tic tac toe.
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

import random

import numpy as np

from tictactoe_qlearning_toy.board import Board

class Player():
    def __init__(self, marker):
        assert marker in 'XO'
        self.marker = marker
        self.mapped_marker = Board.REVERSE_MAPPING[marker]

    def play(self, board):
        raise NotImplementedError('play() not overridden!')

    def reset(self):
        raise NotImplementedError('reset() not overridden!')

class RandomPlayer(Player):
    def play(self, board):
        move = random.choice(np.argwhere(board.board == 0))
        board.board[move] = self.mapped_marker

    def reset(self):
        pass

class MinMaxPlayer(Player):
    def __init__(self, marker):
        super().__init__(marker)

    def play(self, board):
        pass

    def reset(self):
        pass

if __name__ == '__main__':
    b = Board([
        [0, 2, 0],
        [1, 1, 1],
        [0, 0, 2],
    ])
    p = RandomPlayer('X')
    print(p.play(b))
