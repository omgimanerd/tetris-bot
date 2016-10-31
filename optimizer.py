#!/usr/bin/python

from field import Field
from tetromino import Tetromino

from collections import defaultdict

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

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
                    row = f.drop(tetromino_, column)
                    drops.append({
                        'field': f,
                        'orientation': orientation,
                        'column': column,
                        'row': row
                    })
                except AssertionError:
                    continue
        # If it is possible to drop the tetromino and not leave a gap, then we
        # will do so.
        gapless = list(filter(lambda drop: drop['field'].count_gaps() <= gaps,
                              drops))
        if len(gapless) != 0:
            drops = gapless
        # Otherwise, we sort the possible drops by the number of gaps as well
        # as the height that it produces.
        def key(drop):
            return drop['field'].count_gaps() * 100 + (
                100 - drop['row'])
        drops = sorted(drops, key=key)
        assert len(drops) > 0
        return drops[0]

    @staticmethod
    def get_keystrokes(optimal_drop, keymap):
        orientation = optimal_drop['orientation']
        column = optimal_drop['column']
        keys = []
        # First we orient the tetronimo
        if orientation == 1:
            keys.append(keymap['rotate_right'])
        elif orientation == 2:
            keys.append(keymap['rotate_right'])
            keys.append(keymap['rotate_right'])
        elif orientation == 3:
            keys.append(keymap['rotate_left'])
        # Then we move it all the way to the the left that we are guaranteed
        # that it is at column 0. The main reason for doing this is that when
        # thetetromino is rotated, the bottom-leftmost piece in the tetromino
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
    f = Field()
    f.drop(Tetromino.TTetromino(), 3)
    opt = Optimizer.get_optimal_drop(f, Tetromino.ITetromino())
    print(opt['field'])
