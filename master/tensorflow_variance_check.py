from helper_classes import Job, Individual
from queue_handling import WorkManager

i = Individual((1,1,1,1))
j = Job(i)

wm = WorkManager()
scores = []
for i in range(100):
    print(i)
    individual = wm.evaluate([j])
    scores.append(individual[0].score)

with open("variance.txt") as f:
    for score in scores:
        f.write("%s\n" % score)
