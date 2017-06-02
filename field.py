#!/usr/bin/python

from tetromino import Tetromino

import numpy as np

class Field():

    WIDTH = 10
    HEIGHT = 22

    def __init__(self, state=None):
        if state is not None:
            self.state = np.array(state, dtype=np.uint8, copy=True)
        else:
            self.state = np.full((Field.HEIGHT, Field.WIDTH), 0, dtype=np.uint8)

    def __str__(self):
        BAR = '   |' + ' '.join(map(str, range(Field.WIDTH))) + '|\n'
        field = np.vectorize(Tetromino.TYPES.__getitem__)(self.state)
        FIELD = '\n'.join(['{:2d} |'.format(i) +
            ' '.join(row) + '|' for i, row in enumerate(field)])
        return BAR + FIELD + '\n' + BAR

    def _test_tetromino(self, tetromino, row, column):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the bottom left corner of the
        tetromino at the specified row and column.
        """
        r, c = row - tetromino.height(), column + tetromino.width()
        if column < 0 or c > Field.WIDTH:
            return False
        if r < 0 or row >= Field.HEIGHT:
            return False
        for s, t in zip(self.state[r + 1:row + 1, column:c].flat, tetromino.flat()):
            if s and t:
                return False
        return True

    def _place_tetromino(self, tetromino, row, column):
        """
        Place a tetromino at the specified row and column.
        The bottom left corner of the tetromino will be placed at the specified
        row and column. This function does not perform checks and will overwrite
        filled spaces in the field.
        """
        r, c = row - tetromino.height(), column + tetromino.width()
        if column < 0 or c > Field.WIDTH:
            return False
        if r < 0 or row >= Field.HEIGHT:
            return False
        for tr, sr in enumerate(range(r + 1, row + 1)):
            for tc, sc, in enumerate(range(column, c)):
                if tetromino[tr][tc]:
                    self.state[sr][sc] = tetromino[tr][tc]

    def _get_tetromino_drop_row(self, tetromino, column):
        """
        Given a tetromino and a column, return the row that the tetromino
        would end up in if it were dropped in that column.
        Assumes the leftmost column of the tetromino will be aligned with the
        specified column.
        """
        if column < 0 or column + tetromino.width() > Field.WIDTH:
            return -1
        last_fit = -1
        for row in range(tetromino.height(), Field.HEIGHT):
            if self._test_tetromino(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit

    def _line_clear(self):
        """
        Checks and removes all filled lines.
        """
        non_filled = np.array([not row.all() and row.any() for row in self.state])
        if non_filled.any():
            tmp = self.state[non_filled]
            self.state.fill(0)
            self.state[Field.HEIGHT - tmp.shape[0]:] = tmp

    def copy(self):
        """
        Returns a shallow copy of the field.
        """
        return Field(self.state)

    def drop(self, tetromino, column):
        """
        Drops a tetromino in the specified column.
        The leftmost column of the tetromino will be aligned with the specified
        column.
        Returns the row it was dropped in for computations.
        """
        assert isinstance(tetromino, Tetromino)
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        row = self._get_tetromino_drop_row(tetromino, column)
        assert row != -1
        self._place_tetromino(tetromino, row, column)
        self._line_clear()
        return row

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gaps in the
        column.
        """
        gaps = 0
        for col in self.state.T:
            begin = False
            for space in col:
                if space != Tetromino.TYPES_D[' ']:
                    begin = True
                elif begin:
                    gaps += 1
            begin = False
        return gaps

    def heights(self):
        h = Field.HEIGHT - 1
        return np.array([h - np.min(np.nonzero(col)) for col in self.state.T])

    def max_height(self):
        """
        Returns the height on the field of the highest placed tetromino on the
        field.
        """
        return np.max(self.heights())

    def avg_height(self):
        return np.mean(self.heights())

    def dev_height(self):
        return np.std(self.heights())

    def rating(self, weights):
        factors = np.array([
            self.count_gaps(),
            self.max_height(),
            self.avg_height(),
            self.dev_height()
        ])
        return (factors * weights).sum()

if __name__ == '__main__':
    f = Field()
    f.drop(Tetromino.ITetromino(), 6)
    f.drop(Tetromino.ITetromino(), 2)
    f.drop(Tetromino.OTetromino(), 3)
    f.drop(Tetromino.JTetromino().rotate_left(), 0)
    f.drop(Tetromino.JTetromino().rotate_left(), 2)
    f.drop(Tetromino.OTetromino(), 5)
    f.drop(Tetromino.OTetromino(), 7)
    f.drop(Tetromino.ITetromino(), 6)
    f.drop(Tetromino.OTetromino(), 5)
    print(f)
    print(f.count_gaps())
    print(f.max_height())
    print(f.avg_height())
    print(f.dev_height())
    print(f.rating(np.array([ -2, -0.1, -0.2, -1.5])))
    # import sys
    # f = Field()
    # if len(sys.argv) > 1 and sys.argv[1] == 'sim':
    #     from optimizer import Optimizer
    #     i = input()
    #     while i != 'q':
    #         t = Tetromino.create(i)
    #         opt = Optimizer.get_optimal_drop(f, t)
    #         t.rotate(opt['orientation'])
    #         f.drop(t, opt['column'])
    #         print(f)
    #         i = input()
    # t = Tetromino.JTetromino().rotate_right()
    # print(t)
    # f.drop(t, 0)
    # print(f)
    # f.drop(Tetromino.LTetromino(), 2)
    # print(f)
    # f.drop(Tetromino.JTetromino().rotate_left(), 5)
    # print(f)
    # t = Tetromino.LTetromino().flip()
    # f.drop(t, 0)
    # f.drop(Tetromino.TTetromino().flip(), 0)
    # f.drop(Tetromino.JTetromino(), 4)
    # print(f)
