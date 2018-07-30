import random
import copy
import csv
import master.queue_handling as qh
from helper_classes import Job, Individual

seed = 1337
random.seed(seed)

# Generated CNN parameters
m = 5                   # number of bits to encode one layer, eg. for m=5 we get layers in (1;31)
layers = 4              # number of conv layers
N = 100                 # population size
max_iter = 100
max_no_improvement = 50
std_dev = 0.0019255     # std deviation calculated from 100 samples of tf learnings
eps = 4*std_dev         # improvement threshold
crossover_prob = 0.9
mutation_prob = 0.3
keep = 30               # keep best in each population
read_csv = 'newdata.csv'
write_csv = 'newdata2.csv'

wm = qh.WorkManager()


def population_init():
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
    for i in range(N):
        parents.append(copy.deepcopy(select_one(population)))
    return parents


def genotype_to_code(genotype, n, m):
    code = 0
    for i in range(n):
        code += genotype[i]
        code = code << m
    code = code >> m
    return code


def code_to_genotype(code, n, m):
    genotype = []
    for i in range(n):
        genotype.append(code & (2 ** m - 1))
        code = code >> m
    return tuple(genotype[::-1])


def pair_crossover(p1, p2):
    assert len(p1.genotype) == len(p2.genotype) == layers

    n = layers

    mask = random.randint(1, 2 ** (m * n) - 1)
    invmask = 2 ** (m * n) - 1 - mask

    p1code = genotype_to_code(p1.genotype, n, m)
    p2code = genotype_to_code(p2.genotype, n, m)

    d1code = p1code & invmask | p2code & mask
    d2code = p2code & invmask | p1code & mask

    d1 = code_to_genotype(d1code, n, m)
    d2 = code_to_genotype(d2code, n, m)

    return Individual(d1), Individual(d2)


def random_pairs():
    idxs = list(range(N))
    random.shuffle(idxs)
    return [[idxs[i], idxs[i+1]] for i in range(0,N,2)]


def population_crossover(population):
    new_population = []
    for i,j in random_pairs():
        if random.random() < crossover_prob:
            new_population.extend(pair_crossover(population[i], population[j]))
        else:
            new_population.extend((population[i], population[j]))
    return new_population


def perform_mutation(indivdual):
    assert(isinstance(indivdual, Individual))
    which_layer = random.randint(0, layers - 1)
    new_genotype = list(indivdual.genotype)
    new_genotype[which_layer] = random.randint(1,2**m-1)
    indivdual.genotype = tuple(new_genotype)


def population_mutation(population):
    for individual in population:
        if random.random() < mutation_prob:
            perform_mutation(individual)


def fix_broken_individual(individual):
        new_genotype = []
        for layer in individual.genotype:
            if layer < 1:
                new_genotype.append(1)
            else:
                new_genotype.append(layer)
        individual.genotype = tuple(new_genotype)


def fix_broken_population(population):
    for individual in population:
        if 0 in individual.genotype:
            fix_broken_individual(individual)

def map_results_to_dict(results, iter):
    '''

    :param results: list of Individuals
    :return: list of dicts contatining rows for csv writing
    '''
    dicts = []
    for result in results:
        assert(isinstance(result,Individual))
        dicts.append({"iter" : iter,
                      "code" : genotype_to_code(result.genotype, layers, m),
                      "score" : result.score,
                      "loss" : result.loss})
    return dicts


def load_already_computed_from_file():
    reader = csv.reader(open(read_csv, 'r'))
    computed_scores = {}
    for row in reader:
        iter, code, score, loss = row
        computed_scores[code] = (score, loss)
    return computed_scores


def get_already_computed(individual, computed_scores):
    key = str(genotype_to_code(individual.genotype, layers, m))
    if key in computed_scores:
        scores = computed_scores[key]
        individual.score, individual.loss = map(float, scores)


def save_csv(results, iter):
    dicts = map_results_to_dict(results, iter)
    with open(write_csv, 'a') as csvfile:
        fieldnames = ['iter', 'code', 'score', 'loss']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for entry in dicts:
            writer.writerow(entry)


def evaluate_scores(population, workmanager, computed_scores):
    jobs = []
    computed = []
    for individual in population:
        get_already_computed(individual, computed_scores)
        if not individual.score:
            jobs.append(Job(individual, 1, seed))
        else:
            computed.append(individual)
    computed.extend(workmanager.evaluate(jobs))
    return computed


def restore_state_from_file(csvfile):
    reader = csv.reader(open(read_csv, 'r'))
    iters = []
    codes = []
    scores = []
    losses = []
    first = True
    for row in reader:
        # omit header
        if first:
            first = False
            continue
        iter, code, score, loss = row
        iters.append(int(iter))
        codes.append(int(code))
        scores.append(float(score))
        losses.append(float(loss))
    if not iters:
        return False, None, None, None, None
    it = max(iters)
    best_score = max(scores)
    for i, score in enumerate(scores):
        if score == best_score:
            first_max_it = iters[i]
            break
    no_improvement = it - first_max_it
    population = []
    for code in codes:
        population.append(Individual(code_to_genotype(code,layers,m)))
    return True, it, no_improvement, best_score, population


def run():
    with open(write_csv, 'w') as csvfile:
        fieldnames = ['iter', 'genotype', 'score', 'loss']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    computed_scores = load_already_computed_from_file()
    wm = qh.WorkManager()
    restored, it, no_improvement, previous_best_score, population = restore_state_from_file(read_csv)
    print("it: {}, no_improv: {}, best_score: {}".format(it, no_improvement, previous_best_score))
    if not restored:
        population = population_init()
        it = 1
        no_improvement = 0
        previous_best_score = 0
    while it <= max_iter and no_improvement < max_no_improvement:
        print("--------------------------Iter: {}/{}--------------------------------".format(it, max_iter))
        population = evaluate_scores(population, wm, computed_scores)
        population = sorted(population, key=lambda individual: individual.score, reverse=True)
        save_csv(population, it)
        best_score = max(map(lambda x: x.score, population))
        improvement = best_score - previous_best_score
        if improvement > eps:
            no_improvement = 0
            previous_best_score = best_score
        else:
            no_improvement += 1
        parents = selection(population)
        descendants = population_crossover(parents)
        population_mutation(descendants)
        fix_broken_population(descendants)
        # keep best, discard random
        random.shuffle(descendants)
        population[keep:] = descendants[keep:]
        it += 1


if __name__ == '__main__':
    run()
