#!/usr/bin/env python3

from field import Field
from genetic_algorithm import Chromosome, Population
from tetromino import Tetromino

from collections import defaultdict
from functools import cmp_to_key

import numpy as np
import random

class TetrisChromosome(Chromosome):

    GENES = 6
    N_SIMULATIONS = 10
    MAX_SIMULATION_LENGTH = 10000

    def __init__(self):
        self.weights = np.random.random_sample(GENES)
        self.weights /

    def cross(self, other):
        pass

    def score(self):
        tetrominos = [
            Tetromino.ITetromino()
            Tetromino.OTetromino()
            Tetromino.TTetromino()
            Tetromino.STetromino()
            Tetromino.ZTetromino()
            Tetromino.JTetromino()
            Tetromino.LTetromino()
        ]
        field = Field()
        for length in range(MAX_SIMULATION_LENGTH):
            tetromino = random.choice(tetrominos)
            _, __, _field, score = field.get_optimal_drop(
                tetromino, self.weights)
