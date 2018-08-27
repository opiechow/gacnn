import random
import copy
import master.queue_handling as qh
from master.csv_handling import *
import common.params as p
from common.helper_classes import Job, Individual


def population_init(N, m, layers):
    population = []
    for i in range(N):
        population.append(Individual.random(m, layers))
    return population


def select_one(population):
    total = sum(map(lambda x: x.score, population))
    pick = random.uniform(0, total)
    current = 0
    for individual in population:
        current += individual.score
        if current > pick:
            return individual


def selection(population):
    '''
    Implements proportional selection
    :param population: population with scores evaluated
    :return: parents pool
    '''
    parents = []
    for i in range(len(population)):
        parents.append(copy.deepcopy(select_one(population)))
    return parents


def pair_crossover(p1, p2, m=p.m):
    assert len(p1.phenotype) == len(p2.phenotype)

    n = len(p1.phenotype)

    mask = random.randint(1, 2 ** (m * n) - 1)
    invmask = 2 ** (m * n) - 1 - mask

    p1code = phenotype_to_genotype(p1.phenotype, n, m)
    p2code = phenotype_to_genotype(p2.phenotype, n, m)

    d1code = p1code & invmask | p2code & mask
    d2code = p2code & invmask | p1code & mask

    d1 = genotype_to_phenotype(d1code, n, m)
    d2 = genotype_to_phenotype(d2code, n, m)

    return Individual(d1), Individual(d2)


def random_index_pairs(n):
    indexes = list(range(n))
    random.shuffle(indexes)
    return [[indexes[i], indexes[i+1]] for i in range(0, n ,2)]


def crossover(population, crossover_prob):
    new_population = []
    for i,j in random_index_pairs(len(population)):
        if random.random() < crossover_prob:
            new_population.extend(pair_crossover(population[i], population[j]))
        else:
            new_population.extend((population[i], population[j]))
    return new_population


def perform_mutation(indivdual, m=p.m):
    assert(isinstance(indivdual, Individual))
    layers = len(indivdual.phenotype)
    which_layer = random.randint(0, layers - 1)
    new_genotype = list(indivdual.phenotype)
    new_genotype[which_layer] = random.randint(1, 2**m-1)
    indivdual.phenotype = tuple(new_genotype)


def mutation(population, mutation_prob=p.mutation_prob):
    for individual in population:
        if random.random() < mutation_prob:
            perform_mutation(individual)


def fix_broken_individual(individual):
        new_phenotype = []
        for layer in individual.phenotype:
            if layer < 1:
                new_phenotype.append(1)
            else:
                new_phenotype.append(layer)
        individual.phenotype = tuple(new_phenotype)


def fix_broken_population(population):
    for individual in population:
        if 0 in individual.phenotype:
            fix_broken_individual(individual)


def evaluate_scores(population, workmanager, computed_scores, m=5, layers=4, seed=1337):
    jobs = []
    computed = []
    for individual in population:
        get_already_computed(individual, computed_scores, m, layers)
        if not individual.score:
            jobs.append(Job(individual, 1, seed))
        else:
            computed.append(individual)
    computed.extend(workmanager.evaluate(jobs))
    return computed


def restore_state_from_file(read_csv, m, layers, N):
    fresh_start = (False, 1, 0, 0, None)

    if not os.path.isfile(read_csv):
        return fresh_start

    with open(read_csv,'r') as f:
        reader = csv.reader(f)

        iters, codes, scores, losses = [], [], [], []

        next(reader, None)  # skip the header
        for row in reader:
            it, code, score, loss = row
            iters.append(int(it))
            codes.append(int(code))
            scores.append(float(score))
            losses.append(float(loss))

    if not iters:  # nothing to read
        return fresh_start

    it = max(iters)
    best_score = max(scores)

    for i, score in enumerate(scores):
        if score == best_score:
            first_max_it = iters[i]
            break
    no_improvement = it - first_max_it

    population = []
    for code in codes[-N:]:
        population.append(Individual(genotype_to_phenotype(code, layers, m)))

    return True, it, no_improvement, best_score, population


def genetic_operations(population, crossover_prob, mutation_prob, keep):
    parents = selection(population)
    descendants = crossover(parents, crossover_prob)
    mutation(descendants, mutation_prob)
    fix_broken_population(descendants)
    random.shuffle(descendants)
    population[keep:] = descendants[keep:]
    return population


def run():
    random.seed(p.seed)
    create_csv_if_not_existent(p.genetic_write_csv)
    computed_scores = load_already_computed_from_file(p.genetic_read_csv)
    wm = qh.WorkManager()
    restored, it, no_improvement, previous_best_score, population = restore_state_from_file(p.genetic_read_csv, p.m, p.layers, p.N)
    print("it: {}, no_improv: {}, best_score: {}".format(it, no_improvement, previous_best_score))
    if not restored:
        population = population_init(p.N, p.m, p.layers)
    elif it == p.max_iter:
        print("Restored fully conducted experiment. Quitting.")
        return

    while it <= p.max_iter and no_improvement < p.max_no_improvement:
        print("--------------------------Iter: {}/{}--------------------------------".format(it, p.max_iter))
        population = evaluate_scores(population, wm, computed_scores, p.m, p.layers, p.seed)
        population = sorted(population, key=lambda individual: individual.score, reverse=True)
        save_csv_and_history(p.genetic_write_csv, population, it, p.layers, p.m)
        best_score = max(map(lambda x: x.score, population))
        improvement = best_score - previous_best_score
        if improvement > p.eps:
            no_improvement = 0
            previous_best_score = best_score
        else:
            no_improvement += 1
        population = genetic_operations(population, p.crossover_prob, p.mutation_prob, p.keep)
        it += 1


if __name__ == '__main__':
    run()
