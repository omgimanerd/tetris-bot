#!/usr/bin/python

from field import Field
from optimizer import Optimizer
from tetromino import Tetromino

import pyautogui
import time

if __name__ == '__main__':
    field = Field()
    tetromino = None
    key = input()
    while True:
        if key in Tetromino.TYPES:
            tetromino = Tetromino.create(key)
            opt = Optimizer.get_optimal_drop(field, tetromino)
            rotation = opt['tetromino_rotation']
            column = opt['tetromino_column']
            tetromino.rotate(rotation)
            field.drop(tetromino, column)
            keys = Optimizer.get_keystrokes(rotation, column, {
                'rotate_right': 'x',
                'rotate_left': 'z',
                'move_left': 'left',
                'move_right': 'right',
                'drop': ' '
            })
            print(field)
        else:
            print("Invalid input")
        key = input()
