import matplotlib.pyplot as plt

val_acc = [0.4762, 0.523, 0.5539, 0.5789, 0.6005, 0.6145, 0.6247, 0.6313, 0.6368, 0.6398, 0.6434, 0.6496, 0.6535, 0.6564, 0.6598, 0.6622, 0.6628, 0.6653, 0.666, 0.6687, 0.6686, 0.6691, 0.6689, 0.6696, 0.6696]
plt.figure()
plt.plot(val_acc,label='$g_{best}$')
plt.legend(loc=4, prop={'size': 16})
plt.xlabel(r'epoka',fontsize=16)
plt.ylabel(r'$g(x_1, x_2, x_3, x_4)$',fontsize=16)
plt.savefig('25epoch')