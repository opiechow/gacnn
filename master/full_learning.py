import sys
from common.helper_classes import Job, Individual
import master.queue_handling as qh
from master.csv_handling import *

sys.path.append("..")

if __name__ == '__main__':

    filename = "cnn1.csv"

    codes_to_calculate = get_set_of_codes_from_filename(filename, N=100)

    jobs = []
    for code in set(codes_to_calculate):
        jobs.append(Job(Individual(genotype_to_phenotype(code, n=4, m=5)), epochs=10, seed=1337))

    wm = qh.WorkManager()
    calculated = wm.evaluate(jobs)
    save_csv_and_history("zbiorczy.csv", calculated, iteration=0, n=4, m=5)
