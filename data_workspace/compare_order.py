from master.csv_handling import load_already_computed_from_file, phenotype_to_genotype
import csv
import matplotlib.pyplot as plt

class ScoreKeeper(object):
    def __init__(self, genotype, short_score=None, long_score=None):
        self.genotype = genotype
        self.short_score = short_score
        self.long_score = long_score
        self.val_acc_history = None

    def __str__(self):
        return "gen: {}, s.score = {}, l.score = {}".format(self.genotype, self.short_score, self.long_score)

def get_dict_of_histories():
    histories = {}
    with open("2_2/zbiorczy_history.txt",'r') as f:
        for line in f:
            key, value = line.split("|")
            key = key.rstrip()
            phenotype = eval(key)
            true_key = phenotype_to_genotype(phenotype, 4, 5)
            value = value[1:]
            histories[true_key] = eval(value)
    return histories


long_training = load_already_computed_from_file("2_2/zbiorczy.csv")
histories = get_dict_of_histories()

results = []

with open("1_2/cnn1.csv", "r") as f:
    for i, line in enumerate(csv.reader(f)):
        results.append(line)

N = 100

number_of_iterations = int(results[-1][0])  # -1 for last entry, 0 for first field meaning iteration number

best_indexes = [1 + N * i for i in range(number_of_iterations)]
middle_indexes = [N // 2 + N * i for i in range(number_of_iterations)]
worst_indexes = [N * (i + 1) for i in range(number_of_iterations)]

best_list = []
middle_list = []
worst_list = []

for i in best_indexes:
    best_list.append(ScoreKeeper(results[i][1],float(results[i][2])))

for i in middle_indexes:
    middle_list.append(ScoreKeeper(results[i][1],float(results[i][2])))

for i in worst_indexes:
    worst_list.append(ScoreKeeper(results[i][1],float(results[i][2])))

for best in best_list + middle_list + worst_list:
    best.long_score = float(long_training[best.genotype][0])
    best.val_acc_history = histories[int(best.genotype)]['val_acc']

how_much = 0
for i in range(len(best_list)):
    l = (best_list[i], middle_list[i], worst_list[i])
    if sorted(l, key=lambda x:x.short_score) == sorted(l, key=lambda x:x.long_score):
        how_much += 1


plt.rc('font', family='serif')

plt.plot(best_list[0].val_acc_history,label='$g_{best}$')
plt.plot(middle_list[0].val_acc_history,label='$g_{mid}$')
plt.plot(worst_list[0].val_acc_history,label='$g_{worst}$')
plt.legend(loc=4, prop={'size': 16})
plt.xlabel(r'epoka',fontsize=16)
plt.ylabel(r'$g(x_1, x_2, x_3, x_4)$',fontsize=16)
plt.savefig('iter_learn_first')

plt.figure()
plt.plot(best_list[-1].val_acc_history,label='$g_{best}$')
plt.plot(middle_list[-1].val_acc_history,label='$g_{mid}$')
plt.plot(worst_list[-1].val_acc_history,label='$g_{worst}$')
plt.legend(loc=4, prop={'size': 16})
plt.xlabel(r'epoka',fontsize=16)
plt.ylabel(r'$g(x_1, x_2, x_3, x_4)$',fontsize=16)
plt.savefig('iter_learn_last')

plt.figure()
plt.plot(best_list[0].val_acc_history,label='$g_{best}^{start}$')
plt.plot(best_list[-1].val_acc_history,label='$g_{best}^{end}$')
plt.legend(loc=4, prop={'size': 16})
plt.xlabel(r'epoka',fontsize=16)
plt.ylabel(r'$g(x_1, x_2, x_3, x_4)$',fontsize=16)
plt.savefig('iter_learn_firstlastbest')


