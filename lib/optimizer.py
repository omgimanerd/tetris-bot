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
        self.weights = np.random.random_sample(TetrisChromosome.GENES)
        self.fitness = None
        self.field_score = None

    def cross(self, other):
        pass

    def get_fitness(self, simulations=N_SIMULATIONS,
                    simulation_length=MAX_SIMULATION_LENGTH):
        if self.fitness is not None:
            return self.fitness
        scores = np.array([self._get_fitness_(
                simulation_length) for simulation in range(simulations)])
        self.fitness, self.field_score = np.mean(scores, axis=0)
        return self.fitness

    def _get_fitness_(self, simulation_length=MAX_SIMULATION_LENGTH):
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
        field_score = -1
        for length in range(simulation_length):
            tetromino = random.choice(tetrominos)
            _, __, _field, _field_score = field.get_optimal_drop(
                tetromino, self.weights)
            if _field_score == -1:
                return length, field_score
            else:
                field = _field
                field_score = _field_score
        return length, field_score

if __name__ == '__main__':
    c = TetrisChromosome()
    print(c.get_fitness(simulation_length=10))
