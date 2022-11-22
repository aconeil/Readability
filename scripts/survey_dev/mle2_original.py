import datetime
import sys
import numpy
import scipy.stats
import scipy.optimize

sentences = numpy.random.randint(0, 10000, size=100)
comparisons = [
    (min(i,j,key=lambda t: sentences[t]),max(i,j, key=lambda t: sentences[t]))
    for i in numpy.random.randint(0, len(sentences), size=8)
    for j in numpy.random.randint(0, len(sentences), size=8) if i != j
]

print(comparisons)

means = numpy.zeros(len(sentences))
#means = numpy.array([0,2,1,3])
truth = sentences
print("truth: %r" % truth)
cov = numpy.identity(len(sentences))

a = numpy.pi / 4
rot = numpy.array([[numpy.cos(a), numpy.sin(a)], [-numpy.sin(a), numpy.cos(a)]])
rot_T = numpy.transpose(rot)

def rotate_cov(c):
    return rot_T @ c @ rot

def rotate_mean(m):
    return rot_T @ m

def logprob_comparison(m, c):
    try:
        p = scipy.stats.multivariate_normal.logcdf(numpy.array((0, numpy.inf)), mean=rotate_mean(m), cov=rotate_cov(c))
        return p
    except Exception as e:
        return numpy.inf

def logprob_comparisons(comparisons, means, cov):
    p = sum(logprob_comparison(project(means,comparison), project(cov, comparison)) for comparison in comparisons )
    return p
def project(x, indices):
    if len(x.shape) == 1:
        return numpy.array([x[i] for i in indices])
    else:
        return numpy.array([project(x[i], indices) for i in indices])

# extract only the upper triangular entries
def to_ut(c):
    return numpy.array([c[i, j] for i in range(len(c)) for j in range(len(c)) if i <= j])

def from_ut(x):
    ind = [(i, j) for i in range(len(cov)) for j in range(len(cov)) if i <= j]
    return numpy.array([[ x[ind.index((min(i, j),max(i,j)))] for i in range(len(cov))] for j in range(len(cov))])

def objective(x, comparisons):
    return -logprob_comparisons(
        comparisons,
        (( x[:len(sentences)])),
        numpy.diag((( x[len(sentences):])))
    )

def unpack_res(res):
    return (( res.x[:len(sentences)])), numpy.diag((( res.x[len(sentences):])))

dt = datetime.datetime.now()
print("starting base at %s" % dt)
res = scipy.optimize.minimize(
    objective,
    numpy.concatenate((means, numpy.diagonal(cov))),
    args=(comparisons[:-1],),
    options={"ftol":1e-10},
    bounds=scipy.optimize.Bounds(
        lb=0,
        ub=numpy.inf
    )
)

m, c = unpack_res(res)

dt = datetime.datetime.now()
print("starting incremental at %s" % dt)

res2 = scipy.optimize.minimize(
    objective,
    numpy.concatenate((m, numpy.diagonal(c))),
    args=(comparisons,),
    options={"ftol":1e-10},
    bounds=scipy.optimize.Bounds(
        lb=0,
        ub=numpy.inf
    )
)

dt2 = datetime.datetime.now()
print("finished incremental at %s" % dt)

print(dt2 - dt)

dt = datetime.datetime.now()
print("starting full at %s" % dt)
res2 = scipy.optimize.minimize(
    objective,
    numpy.concatenate((m, numpy.diagonal(c))),
    args=(comparisons,),
    options={"ftol":1e-10},
    bounds=scipy.optimize.Bounds(
        lb=0,
        ub=numpy.inf
    )
)

dt2 = datetime.datetime.now()
print("finished full at %s" % dt2)
print(dt2 - dt)
print(res2)


#for c in comparisons:
#    print(m[c[0]] < m[c[1]])
#    if m[c[0]] >= m[c[1]]:
#        print("ugh %r is not less than %r" % (m[c[0]], m[c[1]]))
#        print("but truth says they should be: %r < %r" % (truth[c[0]], truth[c[1]]))
#