#!/usr/bin/env python3

from lib.field import Field
from lib.tetromino import Tetromino
from lib.genetic_algorithm.population import Population

import math
import numpy as np
import random

GENES = 6

class Chromosome():

    N_SIMULATIONS = 4
    MAX_SIMULATION_LENGTH = 1000
    MUTATION_CHANCE = 0.075

    @staticmethod
    def random():
        return Chromosome(Chromosome.random_genes())

    @staticmethod
    def random_genes():
        return (np.random.random_sample(GENES) * 2) - 1

    @staticmethod
    def set_globals(n_simulations, max_simulation_length, mutation_chance):
        Chromosome.N_SIMULATIONS = n_simulations
        Chromosome.MAX_SIMULATION_LENGTH = max_simulation_length
        Chromosome.MUTATION_CHANCE = mutation_chance

    def __init__(self, genes=None):
        self.genes = genes
        self.fitness = None
        self.field_score = None

        self.simulations = Chromosome.N_SIMULATIONS
        self.max_simulation_length = Chromosome.MAX_SIMULATION_LENGTH
        self.mutation_chance = Chromosome.MUTATION_CHANCE

    def __str__(self):
        return '{}\n{}'.format(self.genes, self.fitness)

    def cross(self, other):
        # The genetic values stored in a chromosome are all numeric in the open
        # interval from -1 to 1. When we cross two chromosomes, we will take the
        # weighted average between the genetic values of the two chromosomes,
        # weighting it according to the fitness value of each chromosome.
        #
        # During chromosomal crossing, a mutation has a chance to occur for each
        # genetic value. If one occurs, that genetic value will be set to a new
        # random number in the open interval from -1 to 1.
        w_sum = self.get_fitness() + other.get_fitness()
        genes = (self.genes * self.get_fitness() / w_sum) + (
            other.genes * other.fitness / w_sum)
        mutated_genes = np.random.random_sample(GENES) < self.mutation_chance
        if np.any(mutated_genes):
            nonmutated_genes = mutated_genes == 0
            mutation = Chromosome.random_genes()
            genes = (genes * nonmutated_genes) + (mutation * mutated_genes)
        return Chromosome(genes)

    def get_fitness(self):
        if self.fitness is not None:
            return self.fitness
        self.recalculate_fitness()
        return self.fitness

    def recalculate_fitness(self):
        scores = np.array([
            self._get_fitness_() for _ in range(self.simulations)])
        self.fitness, self.field_score = np.mean(scores, axis=0)

    def _get_fitness_(self):
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
        for length in range(self.max_simulation_length):
            tetromino = random.choice(tetrominos)
            _, __, _field, _field_score = field.get_optimal_drop(
                tetromino, self.genes)
            if _field_score == math.inf:
                return length, field_score
            else:
                field = _field
                field_score = _field_score
        return length, field_score
