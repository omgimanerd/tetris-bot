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

def get_keystrokes(rotation, column, keymap):
    keys = []
    # First we orient the tetronimo
    if rotation == 1:
        keys.append(keymap['rotate_right'])
    elif rotation == 2:
        keys.append(keymap['rotate_right'])
        keys.append(keymap['rotate_right'])
    elif rotation == 3:
        keys.append(keymap['rotate_left'])
    # Then we move it all the way to the the left that we are guaranteed
    # that it is at column 0. The main reason for doing this is that when
    # the tetromino is rotated, the bottom-leftmost piece in the tetromino
    # may not be in the 3rd column due to the way Tetris rotates the piece
    # about a specific point. There are too many edge cases so instead of
    # implementing tetromino rotation on the board, it's easier to just
    # flush all the pieces to the left after orienting them.
    for i in range(4):
        keys.append(keymap['move_left'])
    # Now we can move it back to the correct column. Since pyautogui's
    # typewrite is instantaneous, we don't have to worry about the delay
    # from moving it all the way to the left.
    for i in range(column):
        keys.append(keymap['move_right'])
    keys.append(keymap['drop'])
    return keys


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
