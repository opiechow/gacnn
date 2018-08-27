from master.queue_handling import WorkManager
from common.helper_classes import Individual, Job

wm = WorkManager()
i1 = Individual((1,1,1,1))
i2 = Individual((1,1,1,1))
j1 = Job(i1)
j2 = Job(i2)
l = [j1, j2]
a = wm.evaluate(l)
for r in a:
    print(r)