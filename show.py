#!/usr/bin/env python3
# Author: omgimanerd (Alvin Lin)
#
# Utility script to run a gene against Tetris to simulate and verify its
# performance.
# Invoke with the -h flag for help.

from lib.field import Field
from lib.tetromino import Tetromino
from lib.genetic_algorithm.chromosome import Chromosome

import argparse
import pickle
import random
import time

FIELDS = [
    'Gap Count:\t\t\t{:0.8f}',
    'Mean Column Heights:\t\t{:0.8f}',
    'Stddev Column Heights:\t\t{:0.8f}',
    'Maxmin Height Difference:\t{:0.8f}',
    'Absolute Max ediff1d:\t\t{:0.8f}',
    'ediff1d sum:\t\t\t{:0.8f}'
]

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
    pieces = 0
    while True:
        tetromino = random.choice(tetrominos)
        _, __, field, ___ = field.get_optimal_drop(tetromino, chromosome.genes)
        if field == None:
            break
        print(field)
        pieces += 1
        time.sleep(0.1)
    print('Performance: {}'.format(pieces))

def main():
    parser = argparse.ArgumentParser(
        description='Plays tetris with a given gene file.')
    parser.add_argument('gene', type=argparse.FileType('rb'))
    parser.add_argument(
        '--no_sim',
        help='Show the numeric values in the chromosome instead of simulating '
             'it on Tetris',
        action='store_true')

    args = parser.parse_args()
    with args.gene as gene:
        chromosome = pickle.load(gene)
        if args.no_sim:
            genes = chromosome.genes
            for i, field in enumerate(FIELDS):
                print(field.format(genes[i]))
        else:
            show(chromosome)

if __name__ == '__main__':
    main()
