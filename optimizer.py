#!/usr/bin/python

from field import Field
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
        for orientation, tetromino_ in orientations.items():
            for column in range(Field.WIDTH):
                try:
                    f = field.copy()
                    f.drop(tetromino_, column)
                    fields.append(f)
                except AssertionError:
                    continue
        gapless = list(filter(lambda f: f.count_gaps() <= gaps, fields))
        if len(gapless) != 0:
            fields = gapless
        fields = sorted(fields, key=lambda field: field.height())
        for field in fields:
            print(field)
            print(field.height())

if __name__ == '__main__':
    f = Field()
    # f.drop(Tetromino.TTetromino(), 3)
    Optimizer.get_optimal_drop(f, Tetromino.ITetromino())
