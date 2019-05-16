#!/usr/bin/env python3

class Chromosome():
    def __init__(self):
        raise NotImplementedError

    def cross(self, other):
        raise NotImplementedError

    def get_fitness(self):
        raise NotImplementedError
