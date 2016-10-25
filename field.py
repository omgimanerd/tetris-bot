#!/usr/bin/python

from tetris_exception import TetrisException
from tetromino import Tetromino

import sys

class Field():

    WIDTH = 10
    HEIGHT = 22

    def __init__(self, state=None):
        if state:
            self.state = state
        else:
            self.state = [[' ' for cols in range(Field.WIDTH)]
                          for rows in range(Field.HEIGHT)]

    def __str__(self):
        BAR = '   ' + '-' * (Field.WIDTH * 2 + 1) + '\n    ' + \
            ' '.join(map(str, range(Field.WIDTH))) + '\n'
        return BAR + '\n'.join([
            '{:2d} |'.format(i) + ' '.join(row) + '|'
                for i, row in enumerate(self.state)]) + '\n' + BAR

    def _test_tetromino(self, tetromino, row, column):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the bottom left corner of the
        tetromino at the specified row and column.
        """
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        assert row - tetromino.height() + 1 >= 0
        assert row < Field.HEIGHT
        for ti, si in list(enumerate(range(row - tetromino.height() + 1,
                                           row + 1)))[::-1]:
            for tj, sj in enumerate(range(column, column + tetromino.width())):
                if tetromino[ti][tj] != ' ' and self.state[si][sj] != ' ':
                    return False
        return True

    def _place_tetromino(self, tetromino, row, column):
        """
        Place a tetromino at the specified row and column.
        The bottom left corner of the tetromino will be placed at the specified
        row and column. This function does not perform checks and will overwrite
        filled spaces in the field.
        """
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        assert row - tetromino.height() + 1 >= 0
        assert row < Field.HEIGHT
        for ti, si in list(enumerate(range(row - tetromino.height() + 1,
                                           row + 1)))[::-1]:
            for tj, sj in enumerate(range(column, column + tetromino.width())):
                if tetromino[ti][tj] != ' ':
                    self.state[si][sj] = tetromino[ti][tj]

    def _get_tetromino_drop_row(self, tetromino, column):
        """
        Given a tetromino and a column, return the row that the tetromino
        would end up in if it were dropped in that column.
        Assumes the leftmost column of the tetromino will be aligned with the
        specified column.
        """
        assert isinstance(tetromino, Tetromino)
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        last_fit = -1
        for row in range(tetromino.height(), Field.HEIGHT):
            if self._test_tetromino(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit

    def copy(self):
        return Field([row[:] for row in self.state])

    def drop(self, tetromino, column):
        """
        Drops a tetromino in the specified column.
        The leftmost column of the tetromino will be aligned with the specified
        column.
        """
        assert isinstance(tetromino, Tetromino)
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        row = self._get_tetromino_drop_row(tetromino, column)
        if row != -1:
            self._place_tetromino(tetromino, row, column)
        else:
            raise TetrisException('Unable to place Tetromino: \n{}'.format(
                tetromino))

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gaps in the
        column.
        """
        return sum(
            ["".join([row[col] for row in self.state]).lstrip().count(' ')
             for col in range(Field.WIDTH)])

    def height(self):
        """
        Returns the height on the field of the highest placed tetromino on the
        field.
        """
        for i, row in enumerate(self.state):
            if ''.join(row).strip():
                return Field.HEIGHT - i

if __name__ == '__main__':
    f = Field()
    if len(sys.argv) > 1 and sys.argv[1] == 'sim':
        i = input()
        while i != 'q':
            t = Tetromino.create(i)
            print(t)
            # f.drop(t, f.find_best_column_placement(t))
            print(f)
            i = input()

    f.drop(Tetromino.LTetromino(), 0)
    print(f.height())
    f.drop(Tetromino.LTetromino(), 2)
    f.drop(Tetromino.STetromino(), 2)
    print(f.height())
    t = Tetromino.LTetromino().flip()
    f.drop(t, 0)
    f.drop(Tetromino.TTetromino().flip(), 0)
    f.drop(Tetromino.JTetromino(), 4)
    print(f)
