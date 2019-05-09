#!/usr/bin/env python3

from field import Field
from genetic_algorithm import Chromosome, Population
from tetromino import Tetromino

from collections import defaultdict
from functools import cmp_to_key

import math
import numpy as np
import random
import time

class TetrisChromosome(Chromosome):

    GENES = 6
    N_SIMULATIONS = 5
    MAX_SIMULATION_LENGTH = 1000
    MUTATION_CHANCE = 0.05

    def __init__(self, genes=None):
        if genes is None:
            self.genes = np.random.random_sample(TetrisChromosome.GENES)
        else:
            self.genes = genes
        self.fitness = None
        self.field_score = None

    def __str__(self):
        return '{}\n{}'.format(self.genes, self.fitness)

    def cross(self, other):
        w_sum = self.fitness + other.fitness
        genes = (self.genes * self.fitness / w_sum) + (
            other.genes * other.fitness / w_sum)
        mutated_genes = np.random.random_sample(
            TetrisChromosome.GENES) < TetrisChromosome.MUTATION_CHANCE
        if np.any(mutated_genes):
            nonmutated_genes = mutated_genes == 0
            mutation = np.random.random_sample(TetrisChromosome.GENES)
            genes = (genes * nonmutated_genes) + (mutation * mutated_genes)
        return TetrisChromosome(genes)

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
                tetromino, self.genes)
            if _field_score == math.inf:
                return length, field_score
            else:
                field = _field
                field_score = _field_score
        return length, field_score

    def show(self):
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
        for length in range(500):
            tetromino = random.choice(tetrominos)
            _, __, field, ___ = field.get_optimal_drop(tetromino, self.genes)
            print(field)
            time.sleep(0.25)

if __name__ == '__main__':
    p = Population([TetrisChromosome(
        np.array([0.77681117, 0.3708734, 0.73282138, 0.32482931, 0.12088363,
                  0.15807006])) for i in range(16)])
    for i in range(25):
        p.run()
    member = p.get_fittest_member()
    member.show()
