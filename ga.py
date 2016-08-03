#   Genetic algorithm to optimise a solution for finding a list of N numbers
#   that equal the integer X upon summation
#   e.g. for N = 5, X = 200 possible solutions are 
#   [40,40,40,40,40], [100,20,40,10,30] etc.

N = 10
X = 200000
pop_size=50
from random import randint, random, sample, choice

def individual(length, min, max):
    "Creates a member of the population" 
    return [randint(min,max) for x in range(length)]

def population(count, length, min, max):
    "population of individuals"
    return [individual(length, min, max) for x in range(count)]

def fitness(individual, target):
    # grades fitness of an individual by comparing to target
    return abs(target - sum(individual))

def grade(pop, target):
    # grades fitness of population
    summ = sum([fitness(x,target) for x in pop])
    return(summ / (len(pop)*1.0))


#print(grade(population(10,N,1,X-N),X))
#
#for ind in population(10,N,1,X-N):
#    print("{} {}".format(ind,fitness(ind,X)))

def evolve(pop, X, survival_rate = 0.2, p_mutate = 0.25, random_select = 0.1):
    "Evolve the population"
    def rank(pop, target):
        "return ranked list of pop using fitness" 
        l = []
        for ind in pop:
            l += [[fitness(ind,target), ind]]
        return sorted(l, key = lambda i : i[0])

    def cull(pop, rate):
        "cull the population"
        n_keep = round(len(pop)*rate)
        survive = pop[:n_keep]        
        lucky_ones = sample(pop[n_keep+1:],round(len(pop)*random_select))
        return survive + lucky_ones

    def breed(surv,p_mutate,length):
        "Breed the population and create offspring"
        l = [x[1] for x in surv]
        while len(l) < length:
            mum = choice(l)
            dad = choice(l)
            if mum != dad:
                child = mum[int(len(mum)/2):] + dad[:int(len(dad)/2)]
                l += [child]
        # Now mutate
        for i in range(len(l)):
             l[i] = mutator(l[i],p_mutate)
        return l

    def mutator(ind, p):
        "mutate"
        if random() < p:
            "random chance to mutate"
            mutation_position = randint(0,len(ind)-1)
            print(mutation_position)
            print(ind)
            ind[mutation_position] = randint(min(ind),max(ind))
        return ind

    ranked = rank(pop, X)
    survivors = cull(ranked, survival_rate)
    offspring = breed(survivors,p_mutate,len(pop))
    return offspring

pop = population(pop_size,N,1,X-N)

for i in range(100):
    pop = evolve(pop, X)
    print("----- Iteration {} -----".format(i))
    for ind in pop[:10]:
        print("Individual: {} \n Fitness: {} \n ".format(ind, fitness(ind, X)))
    print("---------------------")

