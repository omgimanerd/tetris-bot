#!/usr/bin/env python3
# Author: omgimanerd (Alvin Lin)
#
# Executable CLI to run the genetic algorithm.
# Parameterizable via command line options, invoke with the -h flag.

from lib.field import Field

from lib.genetic_algorithm.population import Population
from lib.genetic_algorithm.chromosome import Chromosome

import argparse
import pickle

def main():
    parser = argparse.ArgumentParser(description='Runs genetic algorithm.')
    parser.add_argument('outfile', type=argparse.FileType('wb'))

    parser.add_argument('--seed', type=argparse.FileType('rb'))
    parser.add_argument('--generations', type=int, default=25)
    parser.add_argument('--population_size', type=int, default=16)

    parser.add_argument('--n_simulations', type=int,
                        default=Chromosome.N_SIMULATIONS)
    parser.add_argument('--max_simulation_length', type=int,
                        default=Chromosome.MAX_SIMULATION_LENGTH)
    parser.add_argument('--mutation_chance', type=float,
                        default=Chromosome.MUTATION_CHANCE)
    args = parser.parse_args()

    genes = Chromosome.random_genes()
    if args.seed:
        with args.seed as seed:
            chromosome = pickle.load(seed)
            genes = chromosome.genes

    Chromosome.set_globals(args.n_simulations,
                           args.max_simulation_length,
                           args.mutation_chance)
    population = Population([
        Chromosome(genes) for i in range(args.population_size)])
    population.run(args.generations)
    fittest = population.get_fittest_member()

    with args.outfile as outfile:
        pickle.dump(fittest, outfile)
        print('Fittest member: {}'.format(fittest))
        print('Result dumped to {}'.format(outfile))

if __name__ == '__main__':
    main()
