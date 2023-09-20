import datetime
import sys
import numpy as np
import scipy.stats
import scipy.optimize

def best_rankings(m, x):
    relevance = []
    #i is one sentence id in the data
    for i in range(len(m)):
        for j in range(i+1, len(m)):
            #averages of sentences are at the corresponding index in the list m
            mi= m[i]
            mj = m[j]
            #covariance value is at the crossover of i and j in the covariance matrix
            #print(c)
            #print(type(c))
            cii = x[i][i]
            cjj = x[j][j]
            #if there is no comparison for that sentence, go to next pairing
            # if cij == 0:
            #     res = 1000
            #     relevance.append([res, i, j])
            #     continue
            #xbox function with the above variables for i and j
            a = (mi - (2*cii))
            b = (mi + (2*cii))
            c = (mj - (2*cjj))
            d = (mj + (2*cjj))
            p1 = (np.minimum(b, d) - np.maximum(a,c)) / (np.maximum(b, d) - np.minimum(a, c))
            p2 = max((b-a), (d-c))
            res = p1*p2
            #append the value of the relevance along with the sentence ids
            relevance.append([res, i, j])
        relevance = sorted(relevance, key=lambda x: x[0], reverse=True)
    return relevance
