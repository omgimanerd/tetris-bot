#!/usr/bin/env python3

from lib.tetromino import Tetromino

import numpy as np
import math

class Field():

    WIDTH = 10
    HEIGHT = 22
    SCORING_ELEMENTS = 6

    def __init__(self, state=None):
        """
        Initialize a Tetris Field.
        Rows increase downward and columns increase to the right.
        """
        if state is not None:
            self.state = np.array(state, dtype=np.uint8, copy=True)
        else:
            self.state = np.full((Field.HEIGHT, Field.WIDTH), 0, dtype=np.uint8)

    def __str__(self):
        """
        Returns a string representation of the field.
        """
        bar = '   |' + ' '.join(map(str, range(Field.WIDTH))) + '|\n'
        mapped_field = np.vectorize(Tetromino.TYPES.__getitem__)(self.state)
        field = '\n'.join(['{:2d} |'.format(i) +
            ' '.join(row) + '|' for i, row in enumerate(mapped_field)])
        return bar + field + '\n' + bar

    def _test_tetromino_(self, tetromino, r_start, c_start):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the top left corner of the
        tetromino at the specified row and column.
        """
        r_end, c_end = r_start + tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end > Field.HEIGHT:
            return False
        test_area = self.state[r_start:r_end, c_start:c_end]
        for s, t in zip(test_area.flat, tetromino.flat()):
            if s != 0 and t != 0:
                return False
        return True

    def _place_tetromino_(self, tetromino, r_start, c_start):
        """
        Place a tetromino at the specified row and column.
        The bottom left corner of the tetromino will be placed at the specified
        row and column. This function does not perform checks and will overwrite
        filled spaces in the field.
        """
        r_end, c_end = r_start + tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end > Field.HEIGHT:
            return False
        for tr, sr in enumerate(range(r_start, r_end)):
            for tc, sc, in enumerate(range(c_start, c_end)):
                if tetromino[tr][tc] != 0:
                    self.state[sr][sc] = tetromino[tr][tc]

    def _get_tetromino_drop_row_(self, tetromino, column):
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
            if self._test_tetromino_(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit

    def _line_clear_(self):
        """
        Checks and removes all filled lines.
        """
        non_filled = np.array(
            [not row.all() and row.any() for row in self.state])
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
        Returns the row it was dropped in for computations or -1 if a drop was
        unable to be computed.
        """
        assert isinstance(tetromino, Tetromino)
        row = self._get_tetromino_drop_row_(tetromino, column)
        if row == -1:
            return row
        self._place_tetromino_(tetromino, row, column)
        self._line_clear_()
        return row

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gaps in the
        column.
        """
        # Cut off all the empty space above all the placed tetrominos
        top_indices = np.argmax(self.state.T != 0, axis = 1)
        # Count the number of gaps past the first filled space per column
        gaps = [np.count_nonzero(col[top:] == 0) for col, top in zip(
            self.state.T, top_indices)]
        return sum(gaps)

    def heights(self):
        """
        Return an array containing the heights of each column.
        """
        return Field.HEIGHT - np.argmax(self.state.T != 0, axis=1)

    def get_scoring_vector(self):
        """
        Get a vector of values derived from the field used to score a tetromino
        placement.
        """
        heights = self.heights()
        ediff1d = np.ediff1d(heights)
        return np.array([
            self.count_gaps(),             # Gap count
            np.mean(heights),              # Average height
            np.std(heights),               # Standard deviation of heights
            heights.max() - heights.min(), # Max height diff
            abs(ediff1d).max(),            # Max consecutive height diff
            ediff1d.sum()                  # Consecutive height diff sum
        ])

    def get_optimal_drop(self, tetromino, weights=None):
        """
        Given a tetromino and a vector of scoring weights, this method
        calculates the best placement of the tetromino, scoring each placement
        with the weight vector.
        """
        rotations = [
            tetromino,
            tetromino.copy().rotate_right(),
            tetromino.copy().flip(),
            tetromino.copy().rotate_left()
        ]
        best_row, best_column = None, None
        best_field = None
        best_drop_score = math.inf
        for rotation, tetromino_ in enumerate(rotations):
            for column in range(Field.WIDTH):
                f = self.copy()
                row = f.drop(tetromino_, column)
                if row == -1:
                    continue
                scoring_vector = f.get_scoring_vector()
                score = scoring_vector.sum()
                if weights is not None:
                    score = scoring_vector.dot(weights)
                if score < best_drop_score:
                    best_drop_score = score
                    best_row, best_column = (row, column)
                    best_field = f
        return best_row, best_column, best_field, best_drop_score
