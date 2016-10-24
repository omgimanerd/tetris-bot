#!/usr/bin/python

class Tetromino():

    def __init__(self, state, letter):
        self.state = state
        self.letter = letter

    @staticmethod
    def ITetromino():
        return Tetromino(
            [
                ['I'],
                ['I'],
                ['I'],
                ['I']
            ],
            'I'
        )

    @staticmethod
    def OTetromino():
        return Tetromino(
            [
                ['O', 'O'],
                ['O', 'O']
            ],
            'O'
        )

    @staticmethod
    def TTetromino():
        return Tetromino(
            [
                ['T', 'T', 'T']
                [' ', 'T', ' ']
            ],
            'T'
        )

    @staticmethod
    def STetromino():
        return Tetromino(
            [
                [' ', 'S', 'S'],
                ['S', 'S', ' ']
            ],
            'S'
        )

    @staticmethod
    def ZTetromino():
        return Tetromino(
            [
                ['Z', 'Z', ' '],
                [' ', 'Z', 'Z']
            ],
            'Z'
        )

    @staticmethod
    def JTetromino():
        return Tetromino(
            [
                [' ', 'J'],
                [' ', 'J'],
                ['J', 'J']
            ],
            'J'
        )

    @staticmethod
    def LTetromino():
        return Tetromino(
            [
                ['L', ' '],
                ['L', ' '],
                ['L', 'L']
            ],
            'T'
        )

    def __str__(self):
        return "\n".join(["".join(x) for x in self.state])
    
    def rotate_right(self):
        self.state = list(zip(*self.state[::-1]))

    def rotate_left(self):
        self.state = reversed(list(zip(*self.state)))
        
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
