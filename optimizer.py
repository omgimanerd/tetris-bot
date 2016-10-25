#!/usr/bin/python

from field import Field
from tetris_exception import TetrisException
from tetromino import Tetromino

class Optimizer():

    @staticmethod
    def get_optimal_drop(field, tetromino):
        orientations = {
            -1: tetromino.copy().rotate_right(),
            0: tetromino,
            1: tetromino.copy().rotate_left(),
            2: tetromino.copy().flip()
        }
        gaps = field.count_gaps()
        fields = []
        for orientation, tetromino in orientations.items():
            for column in range(Field.WIDTH):
                fields.append

if __name__ == '__main__':
    Optimizer.get_optimal_drop(Field(), Tetromino.LTetromino())
