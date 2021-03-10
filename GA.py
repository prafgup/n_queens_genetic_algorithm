import random
import copy
import math
import numpy as np


#this function calculates number of attacking pairs
def fitness(individual):
    n = len(individual)
    total_collisions = 0
    for i in range(n):
        for j in range(i+1,n):
            diag = abs(individual[j]-individual[i])
            if diag == j - i or diag == 0 :
                total_collisions += 1
    return total_collisions

def crossover(individual1, individual2):
    n = len(individual1)
    crossover_point = random.randint(0,n-1)
    return individual1[0 : crossover_point] + individual2[crossover_point :]


def mutation(individual):
    n = len(individual)

    i = random.randint(0,n-1)
    j = random.randint(0,n-1)
    if j == i:
        j = (j+1)%n
    individual[i], individual[j] = individual[j], individual[i]

    # mutation_point = random.randint(0,n-1)
    # mutation_number = random.randint(1,n)
    # individual[mutation_point] = mutation_number
    return individual
    

def generate_individual(n):
    result = list(range(1, n + 1))
    np.random.shuffle(result)
    return result

class Genetic(object):
    def __init__(self, n ,pop_size):
        #initializing a random individuals with size of initial population entered by user
        self.queens = []
        self.mutation_count = 0
        self.crossover_count = 0
        self.generation_count = 0
        self.current_fittest = n*n
        self.pop_size = pop_size
        for i in range(pop_size):
            self.queens.append(generate_individual(n))

    #generating individuals for a single iteration of algorithm
    def generate_population(self, random_selections=5):
        self.generation_count+=1
        candid_parents = []
        candid_fitness = []
        #getting individuals from queens randomly for an iteration
        for i in range(random_selections):
            candid_parents.append(self.queens[random.randint(0, len(self.queens) - 1)])
            candid_fitness.append((fitness(candid_parents[-1]),i))
        
        #sort the fitnesses of individuals
        sorted_fitness = copy.deepcopy(candid_fitness)
        sorted_fitness.sort()
        
        #getting 2 first individuals(min attackings)
        individual1 = candid_parents[sorted_fitness[0][1]]
        individual2 = candid_parents[sorted_fitness[1][1]]

        crossover_probability = 0.6
        mutation_probability = 0.1

        childrens = []

        #crossover the two parents
        if random.random() < crossover_probability:
            childrens.append(crossover(individual1,individual2))
            self.crossover_count+=1

        # mutation
            if random.random() < mutation_probability:
                childrens[0] = mutation(childrens[0])
                self.mutation_count+=1

        # for parent in candid_parents:
        #     if random.random() < mutation_probability:
        #         childrens.append(mutation(parent))
        #         self.mutation_count+=1

        #in code below check if each child is better than each one of queens individuals, set that individual the new child
        if len(childrens) != 0 :
            if self.queens.count(childrens[0]) > (self.pop_size)//10:
                return
            best_child = childrens[0]
            best_fitness = fitness(best_child)
            for child in childrens:
                if fitness(child) < fitness(best_child):
                    best_child = child
                    best_fitness = fitness(best_child)
            # print(best_child)
            # print(best_fitness)
            for i in range(len(self.queens)):
                if fitness(self.queens[i]) > best_fitness:
                    self.queens[i] = best_child
                    break
            # if self.current_fittest == best_fitness:
            #     i = random.randint(0,len(self.queens)-1)
            #     self.queens[i] = best_child
            #     print("Changed random")



        

    def finished(self):
        for i in self.queens:
            #we check if for each queen there is no attacking(cause this algorithm should work for n queen,
            # it was easier to use attacking pairs for fitness instead of non-attacking)
            ith_fitness = fitness(i)
            self.current_fittest = min(self.current_fittest,ith_fitness)
            if ith_fitness == 0:
                return [True,i]
        return [False,["Not Found"]]

    def start(self, random_selections=5):
        #generate new population and start algorithm until number of attacking pairs is zero
        # self.generate_population(random_selections)
        # return
        while not self.finished()[0]:
            self.generate_population(random_selections)
            #print(self.queens)
            # print("Generation Count = {}".format(self.generation_count))
            # print("Mutation Count = {}".format(self.mutation_count))
            # print("Crossover Count = {}".format(self.crossover_count))
            # print("Fittest Current = {}".format(self.current_fittest))
        final_state = self.finished()
        print("Generation Count = {}".format(self.generation_count))
        print("Mutation Count = {}".format(self.mutation_count))
        print("Crossover Count = {}".format(self.crossover_count))
        print("Fittest Current = {}".format(self.current_fittest))
        print(('Solution : ' + str(final_state[1])))



n=8#(int)(input('Enter the value of N \n -'))
initial_population=20#(int)(input('Enter initial population size \n -'))

algorithm = Genetic(n=n,pop_size=initial_population)
algorithm.start()
