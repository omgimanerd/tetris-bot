#!/usr/bin/python

from field import Field
from optimizer import Optimizer
from tetromino import Tetromino

import pyautogui
import time

TETROMINO = {
    (0, 0, 255): Tetromino.LTetromino,
    (102, 204, 255): Tetromino.STetromino,
    (255, 0, 0): Tetromino.OTetromino,
    (255, 102, 0): Tetromino.ITetromino,
    (204, 0, 255): Tetromino.JTetromino,
    (255, 255, 0): Tetromino.TTetromino,
    (0, 255, 0): Tetromino.ZTetromino
}

def detect_mouse():
    print("Press enter to select mouse coordinate:")
    input()
    return pyautogui.position()

def get_pixel(coordinate):
    return pyautogui.screenshot().getpixel(coordinate)


if __name__ == '__main__':
    mouse = detect_mouse()
    print("Mouse coordinates: {}".format(mouse))
    field = Field()
    print("First tetromino:")
    current_tetromino = Tetromino.create(input())
    next_tetromino = None
    time.sleep(2)
    while True:
        next_tetromino = TETROMINO[get_pixel(mouse)]()
        opt = Optimizer.get_optimal_drop(field, current_tetromino)
        rotation = opt['tetromino_rotation']
        column = opt['tetromino_column']
        current_tetromino.rotate(rotation)
        field.drop(current_tetromino, column)
        keys = Optimizer.get_keystrokes(rotation, column, {
            'rotate_right': 'x',
            'rotate_left': 'z',
            'move_left': 'left',
            'move_right': 'right',
            'drop': ' '
        })
        pyautogui.typewrite(keys)
        print(field)
        current_tetromino = next_tetromino
        time.sleep(0.2)
