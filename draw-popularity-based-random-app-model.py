import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import sys

from math import ceil, floor
def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)
fig = plt.figure()

t1 = list(map(lambda x: x.strip(), open(sys.argv[1]).readlines()))

OX = ['0', '0-0.05', '0.05-0.1', '0.1-0.15', '0.15-0.2', '$>$0.2']
total = int(t1[len(OX)])
OY = []
for i in range(len(OX)):
    OY += [float_round(int(t1[i]) / total, 3, ceil)]



width = .35
ind = np.arange(len(OY))
rects1 = plt.bar(ind, OY, align = 'center')
plt.xticks(ind, OX)
plt.ylabel("Fraction of users")
plt.xlabel("Jaccard coefficient of a user")



def autolabel(rects):
    for rect in rects:
        height = rect.get_height()

        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, "{0:.1f}\%".format(height * 100),
                ha='center', va='bottom')
autolabel(rects1)
plt.yscale('log')
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')


plt.show()