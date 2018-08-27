# This file contains all functions related to csv file handling
# Each function should specify what kind of csv file it expects
from common.helper_classes import Individual
import os
import csv



def get_set_of_codes_from_filename(csv_filename, N):
    """
    Gets all unique codes from a csv file containing first experiment results
    :param N: number of entries per population
    :param csv_filename: the csv file in the form: iter, code, score, loss
    :return: set of unique codes for second experiment
    """
    results = []

    with open(csv_filename, "r") as f:
        for i, line in enumerate(csv.reader(f)):
            results.append(line)

    number_of_iterations = int(results[-1][0])  # -1 for last entry, 0 for first field meaning iteration number

    best_indexes = [1 + N * i for i in range(number_of_iterations)]
    middle_indexes = [N//2 + N * i for i in range(number_of_iterations)]
    worst_indexes = [N*(i+1) for i in range(number_of_iterations)]

    indexes = best_indexes + middle_indexes + worst_indexes
    codes_to_calculate = []

    for i in indexes:
        codes_to_calculate.append(int(results[i][1]))

    return set(codes_to_calculate)


def phenotype_to_genotype(phenotype, n, m):
    """
    Returns the binary representation of the phenotype
    :param phenotype: tuple containing the layer filter numbers
    :param n: number of layers
    :param m: number of bits to encode numbers of layers on
    :return: genotype : binary representation of the phenotype
    """
    code = 0
    for i in range(n):
        code += phenotype[i]
        code = code << m
    code = code >> m
    return code


def genotype_to_phenotype(genotype, n, m):
    """
    Returns the tuple representation of the genotype
    :param genotype : binary representation of the phenotype
    :param n: number of layers
    :param m: number of bits to encode numbers of layers on
    :return: phenotype: tuple containing the layer filter numbers
    """
    phenotype = []
    for i in range(n):
        phenotype.append(genotype & (2 ** m - 1))
        genotype = genotype >> m
    return tuple(phenotype[::-1])


def map_results_to_dicts(results, iteration, n, m):
    """
    Prepares the current iteration's population for csv writing
    :param n:
    :param m:
    :param iteration: iteration number
    :param results: list of Individuals
    :return: list of dicts containing rows for csv writing
    """
    dicts = []
    for result in results:
        assert(isinstance(result, Individual))
        dicts.append({"iter": iteration,
                      "code": phenotype_to_genotype(result.phenotype, n, m),
                      "score": result.score,
                      "loss": result.loss})
    return dicts


def load_already_computed_from_file(read_csv):
    """
    Restores the already stored results in case of resuming the experiment
    :param read_csv: csvfilename to read already stored entries
    :return: a dictionary with already computed
    """
    if not os.path.isfile(read_csv):
        return {}
    reader = csv.reader(open(read_csv, 'r'))
    computed_scores = {}
    for row in reader:
        iteration, code, score, loss = row
        computed_scores[code] = (score, loss)
    return computed_scores


def get_already_computed(individual, computed_scores, m=5, layers=4):
    """
    Modifies an individual in place copying the score from provided dictionary with scores
    :param m:
    :param layers:
    :param individual: indivudial to retrieve the score for
    :param computed_scores: dict contating results, key is genotype, value is (score, loss)
    :return: none, individual modified in place
    """
    key = str(phenotype_to_genotype(individual.phenotype, layers, m))
    if key in computed_scores:
        scores = computed_scores[key]
        individual.score, individual.loss = map(float, scores)


def save_csv_and_history(write_csv, results, iteration, n, m):
    """
    Appends current genetic algorithm
    :param n:
    :param m:
    :param write_csv: filename to append the current iteration results to
    :param results: current population of individuals
    :param iteration: current iteration number
    :return:
    """
    dicts = map_results_to_dicts(results, iteration, n, m)
    with open(write_csv, 'a') as csv_file:
        fieldnames = ['iter', 'code', 'score', 'loss']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for entry in dicts:
            writer.writerow(entry)
    with open(write_csv[:-4] + "_history.txt","a") as f:
        for result in results:
            line = "{:18}| {}\n".format(str(result.phenotype), result.training_history)
            f.write(line)


def create_csv_if_not_existent(write_csv):
    if not os.path.isfile(write_csv):
        with open(write_csv, 'w') as csvfile:
            fieldnames = ['iter', 'genotype', 'score', 'loss']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


if __name__ == '__main__':
    print(genotype_to_phenotype(135586, 4, 5))
    print(genotype_to_phenotype(135454, 4, 5))
