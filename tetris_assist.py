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

def replicate_input(orientation, column):
    keys = []
    # First we orient the piece
    if orientation == 1:
        keys.append('x')
    elif orientation == 2:
        keys.append('x')
        keys.append('x')
    elif orientation == 3:
        keys.append('z')
    # Then we move it all the way to the the left that we are guaranteed
    # that it is at column 0
    keys += ['left', 'left', 'left', 'left']
    # Now we can move it back to the correct column. Since pyautogui's typewrite
    # is instantaneous, we don't have to worry about the delay from moving it
    # all the way to the left.
    for i in range(column):
        keys.append('right')
    keys.append(' ')
    pyautogui.typewrite(keys)
    print(keys)

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
        replicate_input(opt['orientation'], opt['column'])
        print(field)
        print(opt['orientation'], opt['column'])

if __name__ == '__main__':
    keylogger.log(done, key_handler)
