#!/usr/bin/env python3

import random

class Population():
    def __init__(self, population):
        assert len(population) % 4 == 0
        self.population = population
        self.generations = 0

    def run(self, generations):
        cut = len(self.population) // 2
        for i in range(generations):
            population_by_fitness = sorted(
                self.population, key=lambda gene: gene.get_fitness())
            print('Generation: {}'.format(self.generations))
            print([member.get_fitness() for member in population_by_fitness])
            fittest = population_by_fitness[cut:]
            random.shuffle(fittest)
            for i in range(0, cut, 2):
                fittest += [fittest[i].cross(fittest[i + 1])]
                fittest += [fittest[i].cross(fittest[i + 1])]
            self.population = fittest
            self.generations += 1

    def get_fittest_member(self):
        return sorted(self.population, key=lambda gene: gene.get_fitness())[-1]
