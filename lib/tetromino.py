 #!/usr/bin/python

import numpy as np

class Tetromino():

    TYPES = [' ', 'I', 'O', 'T', 'S', 'Z', 'J', 'L']
    TYPES_D = {
        ' ': 0,
        'I': 1,
        'O': 2,
        'T': 3,
        'S': 4,
        'Z': 5,
        'J': 6,
        'L': 7
    }

    def __init__(self, state):
        self.state = np.array(state, dtype=np.uint8, copy=True)

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
            raise ValueError('No Tetromino of type {}'.format(letter))
        return getattr(Tetromino, '{}Tetromino'.format(letter.upper()))()

    def __str__(self):
        return str(np.vectorize(Tetromino.TYPES.__getitem__)(self.state))

    def __getitem__(self, key):
        return self.state[key]

    def copy(self):
        return Tetromino(self.state)

    def flat(self):
        return self.state.flat

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
