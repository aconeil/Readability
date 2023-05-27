import datetime
import numpy as np
import scipy.optimize
from scipy.stats import mvn
from functools import lru_cache
import math

eps_factor = 1E6 * np.finfo(np.dtype('float64')).eps
quantiles = np.array([0, np.inf], dtype=float)
lower = np.array([-np.inf, -np.inf], dtype=float)
maxpts = 2000000
abseps = 1e-5
releps = 1e-5
sqrt2 = np.sqrt(2)
@lru_cache
def logcdf(m1, m2, c1, c2):
    cd = (c1 + c2) / 2.0
    if c1*c2 < cd*eps_factor:
        raise ValueError('singular matrix')
    cod = (c1 - c2) / 2.0
    cov = [[cd, cod], [cod, cd]]
    mean = [(m1-m2)/sqrt2, (m1+m2)/sqrt2]
    return math.log(mvn.mvnun(lower, quantiles, mean, cov, maxpts, abseps, releps)[0])

def mle(comparisons, sentences):
    N = len(sentences)
    def objective(x, comparisons):
        means = x[:N]
        cov = x[N:]
        try:
            return -sum(logcdf(means[a], means[b], cov[a], cov[b]) for a, b in comparisons)
        except:
            return -np.inf

    dt = datetime.datetime.now()
    print("starting base at %s" % dt)
    res = scipy.optimize.minimize(
        objective,
        np.concatenate((np.zeros(N), np.full(N, 1))),
        args=(comparisons[:-1],),
        options={"ftol":1e-10},
        bounds=scipy.optimize.Bounds(
            lb=0,
            ub=np.inf
        )
    )
    #this is the mean and covariance matrix
    return res.x[:N], np.diag(res.x[N:])

