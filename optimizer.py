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
