from helper_classes import Job, Individual
from queue_handling import WorkManager

i = Individual((1,1,1,1))
j = Job(i)

wm = WorkManager()
scores = []
jobs = []

for i in range(100):
    jobs.append(j)

population = wm.evaluate(jobs)

with open("variance.txt",'w') as f:
    for individual in population:
        f.write("%s\n" % individual.score)
