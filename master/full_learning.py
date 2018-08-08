import csv
import sys
from common.helper_classes import Individual
from master.csv_handling import *
from common.params import *

sys.path.append("..")

if __name__ == '__main__':

    filename = "newdata.csv"
    second_filename = "trudata.csv"

    set1 = get_set_of_codes_from_filename(filename)
    set2 = get_set_of_codes_from_filename(second_filename)

    set3 = set2 - set1

    print(set3)

    # jobs = []
    # for code in set(codes_to_calculate):
    #     jobs.append(Job(Individual(code_to_genotype(code,4,5)), epochs=10, seed=1337))
    #
    # single_jobs = [Job(Individual(code_to_genotype(135586, 4, 5)), epochs=25, seed=1337),
    #                Job(Individual(code_to_genotype(135454, 4, 5)), epochs=25, seed=1337)]
    #
    # wm = qh.WorkManager()
    # calculated = wm.evaluate(single_jobs)
    # save_csv(calculated, 0)
