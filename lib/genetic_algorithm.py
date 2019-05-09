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
        assert len(population) % 4 == 0
        self.population = population
        self.generations = 0

    def run(self, generations):
        for i in range(generations):
            cut = len(self.population) // 2
            population_by_fitness = sorted(self.population,
                             key=lambda gene: gene.get_fitness())
            print('Generation: {}'.format(self.generations))
            print([member.fitness for member in population_by_fitness])
            fittest = population_by_fitness[cut:]
            random.shuffle(fittest)
            for i in range(0, cut, 2):
                fittest += [fittest[i].cross(fittest[i + 1])]
                fittest += [fittest[i].cross(fittest[i + 1])]
            print()
            self.population = fittest
            self.generations += 1

    def get_fittest_member(self):
        fittest = sorted(self.population,
                         key=lambda gene: gene.get_fitness())
        print([member.fitness for member in fittest])
        return fittest[-1]
