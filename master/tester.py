import common.helper_classes as hc
import master.queue_handling as qh
from master.csv_handling import genotype_to_phenotype

#p = genotype_to_phenotype(345782, 4, 5)
#print(p)
i = hc.Individual((30,30,30,30))
j = hc.Job(i, epochs=10)
wm = qh.WorkManager()
r = wm.evaluate([j])
i = r[0]
print(i.training_history)