#!/usr/bin/env python

import random

class Chromosome():
    def __init__(self):
        raise NotImplementedError

    def cross(self, other):
        raise NotImplementedError

    def get_fitness(self):
        raise NotImplementedError

class Population():
    def __init__(self, population):
        assert len(population) % 2 == 0
        self.population = population
        self.generations = 0

    def run(self):
        cut = len(self.population) // 2
        fittest = sorted(self.population,
                           key=lambda gene: gene.get_fitness())[:cut]
        random.shuffle(fittest)
        for i in range(0, cut, 2):
            fittest += fittest[i].cross(fittest[i + 1])
        self.population = survivors
        self.generations += 1
