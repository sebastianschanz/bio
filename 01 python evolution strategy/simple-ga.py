######## ___________ SIMPLE GENETIC ALGORITHM ____________ #########
# adapted from Zivia: https://www.youtube.com/watch?v=MZloJByL9s0  #
# __________________ written by Sebastian Schanz __________________#
#
# pandas library as well as cadquery need to be installed initially
# for further information on cadquery python CAD library see:
# https://github.com/CadQuery/CQ-editor#installation
# https://cadquery.readthedocs.io/en/latest/



import cadquery as cq               # for geometry evaluation
import random as rn
import numpy as np                  # for list operations
import pandas as pd                 # for dataset display
import matplotlib.pyplot as plt     # for data visualization



# funny animal names for individuals
fileobj=open('animals.txt')
animals=[]
for line in fileobj:
    animals.append(line.strip())

# funny animal characters for individuals
fileobj=open('adjectives.txt')
adjectives=[]
for line in fileobj:
    adjectives.append(line.strip())



# phenotype parameters
pts_num = 3             # number of points
dim = 2                 # dimensions in space
gen_len = dim*pts_num   # genome length

# genetic algorithm parameters
mut_rate = 0.1
pop_size = 50           # size of population per iteration
generations = 30        # maximal number of iterations in one genetic approach



class individual:
    # individual class that takes a genome, phenotype, fitness and identifies with ID
    def __init__(self):
        self.ID = -1                # identifier keeps track of iterations
        self.genome = -1            # random genome
        self.phenotype = -1         # resulting phenotype
        self.fitness = -1           # fitness computed from phenotype performance
    def data(self):
        data=[str(self.ID), str(self.genome), str(self.phenotype), str(self.fitness)]
        headers=['ID:', 'genome:', 'phenotype:', 'fitness:']
        print(pd.DataFrame(data, headers))



def remap_genome(genome):
    # remaps genome of individual to points in space
    # genome can therefore also be converted in other phenotypes with different transforms
    genome_map = genome*100

    return genome_map



def initialize(pop_size):
    # generates population of size 'pop_size' and safes individuals with genomes of length 'gen_len' to list population[]
    population = []

    for i in range(pop_size):
        population.append(individual())
        population[i].genome = remap_genome(np.random.random_sample((gen_len,))).round(2)
        population[i].phenotype = np.array(population[i].genome.reshape((int(gen_len / dim), dim)), dtype=int).tolist()

    return population



def fitness(population):
    # evaluates the fitness of the generated shapes
    for i in range(len(population)):
        try:
            pts = population[i].phenotype
            wire = cq.Workplane('front')\
            .polyline(pts)\
            .close()\
            .val()
            face = cq.Face.makeFromWires(wire)
            population[i].fitness = int(face.Area())
        except:
            print('Error: CAD could not build geo!')
            population[i].fitness = -1

    return population, face



def selection(population):
    # sorts the population according to the fitness key and selects upper percentage as parents generation
    population = sorted(population, key=lambda population: population.fitness, reverse=True)
    population = population[:int(0.2 * len(population))]

    return population



def crossover(population):
    # cross combines parents until population is refilled
    offspring = []

    for i in range(int((pop_size - len(population)) / 2)):

        parent1 = rn.choice(population)
        parent2 = rn.choice(population)
        child1 = individual()
        child2 = individual()
        split = rn.randint(0, gen_len)
        child1.genome = np.append(parent1.genome[0:split], parent2.genome[split:gen_len])
        child2.genome = np.append(parent2.genome[0:split], parent1.genome[split:gen_len])
        child1.phenotype = np.array(child1.genome.reshape((int(gen_len / dim), dim)), dtype=int).tolist()
        child2.phenotype = np.array(child2.genome.reshape((int(gen_len / dim), dim)), dtype=int).tolist()

        offspring.append(child1)
        offspring.append(child2)

    population.extend(offspring)

    return population



def mutation(population):
    # mutates genome of single individuals randomly
    for i in range(len(population)):

        if rn.uniform(0.0, 1.0) <= mut_rate:
            pos = rn.randint(0, gen_len-1)
            population[i].genome[pos] = round(remap_genome(np.random.random_sample()),2)

    return population



def fitness_avg_calc(population):
    # calculates average fitness for population parts
    avg_fitness = 0
    for i in range(len(population)):
        avg_fitness = avg_fitness + population[i].fitness
    avg_fitness = avg_fitness / len(population)

    return avg_fitness



def visualize_gen(i, generation, gen_fitness, sel_fitness, top_fitness, population):
    # visualizes population as well as the best individuals among them
    plt.ion()

    plt.title('Area Optimization Of Polygon Creatures', fontname = 'monospace')
    plt.plot(generation, top_fitness,           color='darkgrey', label='top fitness',           linewidth=1)
    plt.fill_between(generation, top_fitness,   color='darkgrey')
    plt.plot(generation, sel_fitness,           color='darkgrey', label='selected avg fitness',  linewidth=1)
    plt.fill_between(generation, sel_fitness,   color='lightgrey')
    plt.plot(generation, gen_fitness, ':',      color='darkgrey', label='generation avg fitness',linewidth=1)
    plt.fill_between(generation, gen_fitness,   color='gainsboro')
    if top_fitness[i] != top_fitness[i-1]:
        plt.scatter(generation[i],population[0].fitness, s=30, marker="o",color='steelblue', edgecolors='darkslategrey', linewidths=1, zorder=2.5)
        plt.annotate('%s'%(population[0].ID), (generation[i], top_fitness[i]), fontname = 'monospace', rotation=-45,va='top', color='darkslategrey')
    plt.xlabel('Generation', fontname = 'monospace')
    plt.ylabel('Fitness', fontname = 'monospace')
    # plt.legend(loc='lower right')

    plt.show()
    plt.draw()
    plt.pause(0.001)

    if generation[i] == generations-1:
        plt.savefig('evolution_overview.png')



def ga(generations):

    generation = []
    gen_fitness = []
    sel_fitness = []
    top_fitness = []

    population = initialize(pop_size)

    for i in range(generations):
        print('GENEARTION: ' + str(i))

        generation.append(i)

        population, face = fitness(population)
        cq.show_object(face)
        gen_fitness.append(fitness_avg_calc(population))

        population = selection(population)

        sel_fitness.append(fitness_avg_calc(population))
        top_fitness.append(population[0].fitness)

        population = crossover(population)
        population = mutation(population)

        for j in range(len(population)):               #print population routine
            population[j].ID = 'G%d, %s %s' %(i, rn.choice(adjectives), rn.choice(animals))
            # population[j].data() # print all individuals of a generation

        visualize_gen(i, generation, gen_fitness, sel_fitness, top_fitness, population)
        # population[0].data() # print top individual per generation

    return population



final_population = ga(generations)
final_population[0].data()

###################### CONTINUE HERE ##########################
# points must be reinstated to individual, what is best practice? inputs, or create on fly...
# then the area must be calculated as fitness
#
# encode genome differently
#
# optimize result of artificial evolution with gradient decent
# training data could be performance of single individuals
#
#

# namen in genom codieren, jupyter notebook, googly eyes
