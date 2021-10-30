import numpy as np
import math
import sys


def consolidateDataDiscreteUnifs(vals):
    consolidated_vals = []
    consolidated_probs = []

    for val in vals:
        if val in consolidated_vals:
            continue
        else:
            consolidated_vals.append(val)

    for val in consolidated_vals:
        consolidated_probs.append(0)
    
    for val in vals:
        index = consolidated_vals.index(val)
        consolidated_probs[index]+=(1/len(vals))

    
    return consolidated_vals,consolidated_probs



def computeCDFFromPDF(vals,probs):
    # P(X <= x)

    cdf_probs = [probs[0]]
    for prob in probs[1:]:
        cdf_probs.append(prob + cdf_probs[-1])
    return cdf_probs

def computeZeroOrderStatDiscreteUnif(vals,N):
    order_stat_probs = []

    consolidated_vals,consolidated_probs = consolidateDataDiscreteUnifs(vals)

    consolidated_vals_cdf = computeCDFFromPDF(consolidated_vals,consolidated_probs)

    for i,val in enumerate(consolidated_vals):
        sum = 0

        for m in range(N):
            term_to_add = (math.factorial(N) * (consolidated_probs[i])**(m+1) * (1-consolidated_vals_cdf[i])**(N-m-1) )/(math.factorial(m+1) * math.factorial(N-m-1))
            sum += term_to_add
        order_stat_probs.append(sum)
    
    assert abs(np.sum(order_stat_probs)-1) < 0.0001
    return consolidated_vals,order_stat_probs



def main(probs_file):
    probs = np.load(probs_file)
    probs.sort() # data needs to be sorted in ascending order
    N = 100 # number of schedulers used in lss
    os_0_vals,os_0_probs = computeZeroOrderStatDiscreteUnif(probs,N)


if __name__ == "__main__":
    dist_path = sys.argv[1]
    main(dist_path)








