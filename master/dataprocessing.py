import csv
import matplotlib.pyplot as plt
import numpy as np

maxes = []
means = []
first = True
with open("maxmean.csv","r") as f:
    rd = csv.reader(f)
    for row in rd:
        maxes.append(float(row[0]))
        means.append(float(row[1]))

plt.rc('font', family='serif')

plt.plot(maxes,label='$g_{max}$')
plt.ylim([975, 1005])
plt.legend(loc=4, prop={'size': 16})
plt.xlabel(r'pokolenie',fontsize=16)
plt.ylabel(r'$g(x_1, x_2, x_3, x_4)$',fontsize=16)
plt.savefig('levy_maxes')

plt.figure()
plt.plot(means,'-.',label='$g_{avg}$')
plt.legend(prop={'size': 16})
plt.xlabel(r'pokolenie',fontsize=16)
plt.ylabel(r'$g(x_1, x_2, x_3, x_4)$',fontsize=16)
plt.savefig('levy_means')
