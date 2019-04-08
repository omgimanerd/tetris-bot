#!/usr/bin/env python

import random

class Gene():
    def __init__(self):
        raise NotImplementedError

    def cross(self, other):
        raise NotImplementedError

    def get_fitness(self):
        raise NotImplementedError

class Pool():
    def __init__(self, pool):
        assert len(pool) % 2 == 0
        self.pool = pool
        self.generations = 0

    def run(self):
        cut = len(self.pool) // 2
        survivors = sorted(self.pool, key=lambda gene: gene.get_fitness())[:cut]
        random.shuffle(survivors)
        for i in range(0, cut, 2):
            survivors += survivors[i].cross(survivors[i + 1])
        self.pool = survivors
        self.generations += 1
