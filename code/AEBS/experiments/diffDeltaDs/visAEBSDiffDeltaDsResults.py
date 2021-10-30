import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt
from pylab import *



##############################
## N5 H5
##############################
N=1
H=3
L=3


carlaLowerBound = 1-4/100
carlaUpperBound = 1-10/100


# baseline results
runTimesBaseline = np.load('../../../../results/AEBS/diffDeltaDs_MC/baseline/runtimesAEBSBaseline.npy')[:-1]
safetyProbsBaseline = np.load('../../../../results/AEBS/diffDeltaDs_MC/baseline/safetyProbsAEBSBaseline.npy')[:-1]

plt.scatter(runTimesBaseline,safetyProbsBaseline,color='green',marker='s',s=100)

# trimmed baseline results
runTimesBaseline = np.load('../../../../results/AEBS/diffDeltaDs_MC/trimmedBaseline_MC/runtimesAEBSBaselineMC.npy')[:-1]
safetyProbsBaseline = np.load('../../../../results/AEBS/diffDeltaDs_MC/trimmedBaseline_MC/safetyProbsAEBSBaselineMC.npy')[:-1]

plt.scatter(runTimesBaseline,safetyProbsBaseline,color='red',marker='o',s=100)

# plt.legend(fontsize=40)
plt.legend(['Baseline','Trimmed'],loc='lower right',fontsize = 20)

ax = plt.gca()
ax.set_ylim([0,1])
xs = np.arange(0.05,6500,1)


plt.hlines(y=carlaLowerBound,xmin=0,xmax=60000,color='orange',linestyle="dotted")
plt.hlines(y=carlaUpperBound,xmin=0,xmax=60000,color='orange',linestyle="dotted")

ax.fill_between(xs,carlaLowerBound,carlaUpperBound,color='orange',alpha=0.2)

ax.set_xscale('log')
ax.set_xlim([1,100])
plt.xlabel('Run time (s)',fontsize=20)
plt.ylabel('Safety Probability',fontsize=20)
# plt.title('Abstraction Accuracy v. Runtime Tradeoff')
# plt.savefig('../../../../results/AEBS/diffDeltaDs_MC/plots/AEBSDiffDeltaDsPlot.png')
plt.show()