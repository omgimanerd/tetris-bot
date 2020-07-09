"""
The Board class encapsulates functionality for manipulating a tic tac toe
board.
"""
# pylint: disable=missing-function-docstring

import numpy as np

class Board():
    """
    Class encapsulating tic tac toe board for toy qlearning example.
    """

    MAPPING = {
        0: '-',
        1: 'X',
        2: 'O'
    }

    REVERSE_MAPPING = {
        '-': 0,
        'X': 1,
        'O': 2
    }

    def __init__(self, board=None):
        if board is not None:
            assert len(board) == 3
            assert len(board[0]) == 3
            self.board = np.array(board)
        else:
            self.board = np.zeros(shape=(3, 3))

    def __str__(self):
        return '\n'.join([
            ''.join([
                Board.MAPPING[c] for c in row]) for row in self.board])

    def get_winner(self):
        for row in self.board:
            if np.all(row == row[0]) and row[0] != 0:
                return row[0]
        for col in self.board.T:  # pylint: disable=not-an-iterable
            if np.all(col == col[0]) and col[0] != 0:
                return col[0]
        diagonal = np.array([0, 1, 2])
        if (
                np.all(self.board[diagonal, diagonal] == self.board[0, 0])
                and self.board[0, 0] != 0
        ):
            return self.board[0, 0]
        if (
                np.all(self.board[diagonal, diagonal[::-1]] == self.board[0, 2])
                and self.board[0, 2] != 0
        ):
            return self.board[0, 2]
        return None

    def copy(self):
        return Board(board=np.copy(self.board))

if __name__ == '__main__':
    b = Board([
        [0, 2, 0],
        [1, 1, 1],
        [0, 0, 2],
    ])
    print(b)
    print(b.get_winner())
