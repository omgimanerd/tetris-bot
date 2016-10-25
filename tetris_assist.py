#!/usr/bin/python

from field import Field
from optimizer import Optimizer
from tetromino import Tetromino

import keylogger

field = Field()
quit = False

def done():
    return quit

def key_handler(time, modifiers, keys):
    print(keys)

if __name__ == '__main__':
    keylogger.log(done, key_handler)
