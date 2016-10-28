#!/usr/bin/python

from field import Field
from optimizer import Optimizer
from tetromino import Tetromino

import keylogger

import pyautogui
import time

pyautogui.PAUSE = 0

field = Field()
tetromino = None
quit = False

def done():
    return quit

def key_handler(time, modifiers, key):
    mapping = {
        '1': 'i',
        '2': 'o',
        '3': 't',
        '4': 's',
        '5': 'z',
        '6': 'j',
        '7': 'l'
    }
    if key and key in mapping:
        tetromino = Tetromino.create(mapping[key])
        opt = Optimizer.get_optimal_drop(field, tetromino)
        tetromino.rotate(opt['orientation'])
        field.drop(tetromino, opt['column'])
        keys = Optimizer.get_keystrokes(opt, {
            'rotate_right': 'x',
            'rotate_left': 'z',
            'move_left': 'left',
            'move_right': 'right',
            'drop': ' '
        })
        pyautogui.typewrite(keys)
        print(field)
        print(keys)

if __name__ == '__main__':
    keylogger.log(done, key_handler)
