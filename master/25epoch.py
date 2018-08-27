import common.helper_classes as hc
import master.queue_handling as qh
from master.csv_handling import genotype_to_phenotype, save_csv_and_history

# 657054
# 656867

codes = [415487]
jobs = []
for code in codes:
    p1 = genotype_to_phenotype(code, 4, 5)
    i1 = hc.Individual(p1)
    j1 = hc.Job(i1, epochs=25)
    jobs.append(j1)
wm = qh.WorkManager()
r = wm.evaluate(jobs)
save_csv_and_history("best.csv", r, 0, 4, 5)