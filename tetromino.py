#!/usr/bin/python

import numpy as np

class Tetromino():

    TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

    def __init__(self, state, copy=False):
        self.state = np.array(state, copy=copy)

    @staticmethod
    def ITetromino():
	    return Tetromino(
            [
                ['I', 'I', 'I', 'I']
            ]
        )

    @staticmethod
    def OTetromino():
        return Tetromino(
            [
                ['O', 'O'],
                ['O', 'O']
            ]
        )

    @staticmethod
    def TTetromino():
        return Tetromino(
            [
                ['T', 'T', 'T'],
                [' ', 'T', ' ']
            ]
        )

    @staticmethod
    def STetromino():
        return Tetromino(
            [
                [' ', 'S', 'S'],
                ['S', 'S', ' ']
            ]
        )

    @staticmethod
    def ZTetromino():
        return Tetromino(
            [
                ['Z', 'Z', ' '],
                [' ', 'Z', 'Z']
            ]
        )

    @staticmethod
    def JTetromino():
        return Tetromino(
            [
                ['J', 'J', 'J'],
                [' ', ' ', 'J']
            ]
        )

    @staticmethod
    def LTetromino():
        return Tetromino(
            [
                ['L', 'L', 'L'],
                ['L', ' ', ' ']
            ]
        )

    @staticmethod
    def create(letter):
        if letter.upper() in Tetromino.TYPES:
            raise ValueError('Could not create Tetromino of type {}'.format(letter))
        return getattr(Tetromino, '{}Tetromino'.format(letter.upper()))()

    def __str__(self):
        return np.array2string(self.state)

    def __getitem__(self, key):
        return self.state[key]

    def copy(self):
        return Tetromino(self.state, copy=True)

    def width(self):
        return self.state.shape[1]

    def height(self):
        return self.state.shape[0]

    def rotate(self, change):
        while change < 0:
            change += 4
        change = (change % 4)
        if change == 0:
            return None
        elif change == 1:
            self.rotate_right()
        elif change == 2:
            self.flip()
        elif change == 3:
            self.rotate_left()

    def rotate_right(self):
        self.state = np.rot90(self.state, 3)
        return self

    def rotate_left(self):
        self.state = np.rot90(self.state, 1)
        return self

    def flip(self):
        self.state = np.rot90(self.state, 2)
        return self

if __name__ == '__main__':
    t = Tetromino.LTetromino()
    print(t)
    t.rotate_right()
    print(t)
    t.rotate_right()
    print(t)
    t.rotate_left()
    print(t)
    print(t.height())
    print(t.width())
    t.flip()
    print(t)
    print(t.state.dtype)
    q = t.copy()
    q.rotate_left()
    print(t)
    print(q)
