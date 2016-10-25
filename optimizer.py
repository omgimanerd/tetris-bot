#!/usr/bin/python

from field import Field
from tetromino import Tetromino

from collections import defaultdict

class Optimizer():

    @staticmethod
    def get_optimal_drop(field, tetromino):
        orientations = [
            tetromino,
            tetromino.copy().rotate_right(),
            tetromino.copy().flip(),
            tetromino.copy().rotate_left(),
        ]
        gaps = field.count_gaps()
        drops = []
        for orientation, tetromino_ in enumerate(orientations):
            for column in range(Field.WIDTH):
                try:
                    f = field.copy()
                    f.drop(tetromino_, column)
                    drops.append({
                        'field': f,
                        'orientation': orientation,
                        'column': column
                    })
                except AssertionError:
                    continue
        # Sometimes it might be strategic to leave a gap. Account for this.
        gapless = list(filter(lambda drop: drop['field'].count_gaps() <= gaps,
                              drops))
        if len(gapless) != 0:
            drops = gapless
        drops = sorted(drops, key=lambda drop: drop['field'].height())
        assert len(drops) > 0
        return drops[0]

if __name__ == '__main__':
    f = Field()
    f.drop(Tetromino.TTetromino(), 3)
    opt = Optimizer.get_optimal_drop(f, Tetromino.ITetromino())
    print(opt['field'])
