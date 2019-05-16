#!/usr/bin/env python3

from lib.field import Field
from lib.tetromino import Tetromino
from lib.genetic_algorithm.chromosome import Chromosome

import argparse
import pickle
import random
import time

def show(chromosome):
    tetrominos = [
        Tetromino.ITetromino(),
        Tetromino.OTetromino(),
        Tetromino.TTetromino(),
        Tetromino.STetromino(),
        Tetromino.ZTetromino(),
        Tetromino.JTetromino(),
        Tetromino.LTetromino()
    ]
    field = Field()
    while True:
        tetromino = random.choice(tetrominos)
        _, __, field, ___ = field.get_optimal_drop(tetromino, chromosome.genes)
        if field == None:
            break
        print(field)
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(
        description='Plays tetris with a given chromosome result.')
    parser.add_argument('infile', type=argparse.FileType('rb'))
    args = parser.parse_args()
    with args.infile as infile:
        chromosome = pickle.load(infile)
        show(chromosome)

if __name__ == '__main__':
    main()
