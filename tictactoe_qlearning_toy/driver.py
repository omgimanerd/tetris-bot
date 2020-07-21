"""
The Driver class runs a game of tic tac toe with two players.
"""
# pylint: disable=missing-function-docstring

import random

from collections import defaultdict

from tictactoe_qlearning_toy.board import Board
from tictactoe_qlearning_toy.player import RandomPlayer

class Driver():
    def __init__(self, player_o, player_x, turn):
        assert player_o.marker == 'O'
        assert player_x.marker == 'X'
        assert turn in 'OX'
        self.player_o = player_o
        self.player_x = player_x
        self.turn = turn
        self.winner = None
        self.board = Board()

    def reset(self, turn):
        self.player_o.reset()
        self.player_x.reset()
        self.turn = turn
        self.winner = None
        self.board.reset()

    def play(self):
        while self.winner is None:
            if self.turn == 'O':
                self.player_o.play(self.board)
            elif self.turn == 'X':
                self.player_x.play(self.board)
            else:
                raise ValueError('Wtf whose turn is it?')
            self.winner = self.board.get_winner()
        return Board.MAPPING[self.winner]

if __name__ == '__main__':
    d = Driver(RandomPlayer('O'), RandomPlayer('X'), random.choice('XO'))
    wins = defaultdict(int)
    for i in range(10000):
        winner = d.play()
        wins[winner] += 1
        d.reset(random.choice('XO'))
    print(wins)
