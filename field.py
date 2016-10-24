#!/usr/bin/python

from tetromino import Tetromino

class TetrisException(Exception):
    pass

class Field():

    WIDTH = 10
    HEIGHT = 22

    def __init__(self):
        self.state = [[' ' for cols in range(Field.WIDTH)]
                      for rows in range(Field.HEIGHT)]

    def __str__(self):
        for i in self.state:
            print(i)
        BAR = '   ' + '-' * (Field.WIDTH * 2 + 1)
        return BAR + '\n' + '\n'.join([
            '{:2d} |'.format(i) + ' '.join(row) + '|'
                for i, row in enumerate(self.state)]) + '\n' + BAR

    def _test_tetromino(self, tetromino, row, column):
        assert column + tetromino.width() <= Field.WIDTH
        assert row - tetromino.height() + 1 >= 0
        for ti, si in list(enumerate(range(row - tetromino.height() + 1,
                                           row + 1)))[::-1]:
            for tj, sj in enumerate(range(column, column + tetromino.width())):
                if tetromino[ti][tj] != ' ' and self.state[si][sj] != ' ':
                    return False
        return True

    def _place_tetromino(self, tetromino, row, column):
        assert column + tetromino.width() <= Field.WIDTH
        assert row - tetromino.height() + 1 >= 0
        for ti, si in list(enumerate(range(row - tetromino.height() + 1,
                                           row + 1)))[::-1]:
            for tj, sj in enumerate(range(column, column + tetromino.width())):
                self.state[si][sj] = tetromino[ti][tj]

    def drop(self, tetromino, column):
        assert isinstance(tetromino, Tetromino)
        assert column + tetromino.width() <= Field.WIDTH
        for row in range(Field.HEIGHT)[::-1]:
            print(row)
            if self._test_tetromino(tetromino, row, column):
                self._place_tetromino(tetromino, row, column)
                return
        raise TetrisException('Unable to place Tetromino: \n{}'.format(
            tetromino))

if __name__ == '__main__':
    f = Field()
    f.drop(Tetromino.LTetromino(), 0)
    f.drop(Tetromino.LTetromino(), 2)
    f.drop(Tetromino.STetromino(), 7)
    print(f)
