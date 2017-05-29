#!/usr/bin/python

import numpy as np

class Tetromino():

    TYPES = [' ', 'I', 'O', 'T', 'S', 'Z', 'J', 'L']

    def __init__(self, state, copy=False):
        self.state = np.array(state, dtype=np.int8, copy=False)

    @staticmethod
    def ITetromino():
		return Tetromino(
            [
                [1, 1, 1, 1]
            ]
        )

    @staticmethod
    def OTetromino():
        return Tetromino(
            [
                [2, 2],
                [2, 2]
            ]
        )

    @staticmethod
    def TTetromino():
        return Tetromino(
            [
                [3, 3, 3],
                [0, 3, 0]
            ]
        )

    @staticmethod
    def STetromino():
        return Tetromino(
            [
                [0, 4, 4],
                [4, 4, 0]
            ]
        )

    @staticmethod
    def ZTetromino():
        return Tetromino(
            [
                [5, 5, 0],
                [0, 5, 5]
            ]
        )

    @staticmethod
    def JTetromino():
        return Tetromino(
            [
                [6, 6, 6],
                [0, 0, 6]
            ]
        )

    @staticmethod
    def LTetromino():
        return Tetromino(
            [
                [7, 7, 7],
                [7, 0, 0]
            ]
        )

    @staticmethod
    def create(letter):
        if letter.upper() in Tetromino.TYPES[1:]:
			raise ValueError('Could not create Tetromino of type {}'.format(letter))
        return getattr(Tetromino, '{}Tetromino'.format(letter.upper()))()

    def __str__(self):
        return "\n".join(self.state)

    def __getitem__(self, key):
        return self.state[key]

    def copy(self):
        return Tetromino(self.state, copy=True)

    def width(self):
        return len(self.state[0])

    def height(self):
        return len(self.state)

    def rotate(self, change):
        while change < 0:
            change += 4
        change = (change % 4)
        assert 0 <= change and change <= 3
        if change == 0:
            return None
        elif change == 1:
            self.rotate_right()
        elif change == 2:
            self.flip()
        elif change == 3:
            self.rotate_left()
        else:
            raise Exception('This should never happen!')

    def rotate_right(self):
        self.state = list(zip(*self.state[::-1]))
        return self

    def rotate_left(self):
        self.state = list(reversed(list(zip(*self.state))))
        return self

    def flip(self):
        self.state = [row[::-1] for row in self.state[::-1]]
        return self

if __name__ == '__main__':
    t = Tetromino.LTetromino()
    print(t)
    print()
    t.rotate_right()
    print(t)
    print()
    t.rotate_right()
    print(t)
    print()
    t.rotate_left()
    print(t)
    print(t.height())
    print(t.width())
    t.flip()
    print(t)
