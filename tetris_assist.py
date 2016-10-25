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

START_COLUMN = 3

def done():
    return quit

def replicate_input(orientation, column):
    keys = []
    if orientation == 1:
        keys.append('x')
    elif orientation == 2:
        keys.append('x')
        keys.append('x')
    elif orientation == 3:
        keys.append('z')

    c = column - START_COLUMN
    print(c)
    if c > 0:
        for i in range(c):
            keys.append('right')
    else:
        for i in range(abs(c)):
            keys.append('left')
    keys.append(' ')
    for key in keys:
        pyautogui.keyDown(key)
        time.sleep(0.04)
        pyautogui.keyUp(key)
    print(keys)


def key_handler(time, modifiers, key):
    if key and key.lower() in ['i', 'o', 't', 's', 'z', 'j', 'l']:
        tetromino = Tetromino.create(key)
        opt = Optimizer.get_optimal_drop(field, tetromino)
        tetromino.rotate(opt['orientation'])
        field.drop(tetromino, opt['column'])
        replicate_input(opt['orientation'], opt['column'])
        print(field)
        print(opt['orientation'], opt['column'])

if __name__ == '__main__':
    keylogger.log(done, key_handler)
