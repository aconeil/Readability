import datetime
import sys
import numpy
import scipy.stats
import scipy.optimize

#sentences equal a random list of 100 integers in the range 0-10000
sentences = numpy.random.randint(0, 10000, size=100)
#comparisons are minimum value of i and j and maximum value of i and j for sentences at index t in the list
#this should come from the main.py code
# comparisons is a list of pairs (i, j) where i is easier/? than j
comparisons = [
    (min(i,j,key=lambda t: sentences[t]),max(i,j, key=lambda t: sentences[t]))
    #size equals 8 sets us to compare only 8 sentences?
    for i in numpy.random.randint(0, len(sentences), size=8)
    for j in numpy.random.randint(0, len(sentences), size=8) if i != j
]


def run_xbox(sentences, comparisons):
    # comparisons = list of pairs of comparisons, e.g. [(1,3), (3,4), (4, 5)] where numbers are sentence indexes
    # sentences = a list of sentence ids


    print(comparisons)

    #means are an array in the shape of length of sentences with all values set to zero
    means = numpy.zeros(len(sentences))
    #means = numpy.array([0,2,1,3])
    #value truth corresponds to list of sentences
    truth = sentences
    print("truth: %r" % truth)
    #set covariance to an array with ones along the diag the size of the length of sentences list
    cov = numpy.identity(len(sentences))

    # how to rotate a matrix
    a = numpy.pi / 4
    rot = numpy.array([[numpy.cos(a), numpy.sin(a)], [-numpy.sin(a), numpy.cos(a)]])
    rot_T = numpy.transpose(rot)

    #rotate the covariance matrix
    def rotate_cov(c):
        return rot_T @ c @ rot

    # rotate the mean
    def rotate_mean(m):
        return rot_T @ m
    #compare the log probability of the mean to the covariance
    def logprob_comparison(m, c):
        try:
            p = scipy.stats.multivariate_normal.logcdf(numpy.array((0, numpy.inf)), mean=rotate_mean(m), cov=rotate_cov(c))
            return p
        except Exception as e:
            return numpy.inf

    # return a value to base the comparisons on based on the means and covariance of each comparison
    def logprob_comparisons(comparisons, means, cov):
        p = sum(logprob_comparison(project(means,comparison), project(cov, comparison)) for comparison in comparisons )
        return p

    #what is x and what are the indices
    def project(x, indices):
        if len(x.shape) == 1:
            return numpy.array([x[i] for i in indices])
        else:
            return numpy.array([project(x[i], indices) for i in indices])

    # extract only the upper triangular entries
    def to_ut(c):
        return numpy.array([c[i, j] for i in range(len(c)) for j in range(len(c)) if i <= j])
    # create an array for the minimum and maximum values of i and j
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

#dt = datetime.datetime.now()
#print("starting base at %s" % dt)
#
#res = scipy.optimize.minimize(
#    objective,
#    numpy.concatenate((means, numpy.diagonal(cov))),
#    args=(comparisons[:-1],),
#    options={"ftol":1e-10},
#    bounds=scipy.optimize.Bounds(
#        lb=0,
#        ub=numpy.inf
#    )
#)
#
#m, c = unpack_res(res)
#
#dt = datetime.datetime.now()
#print("starting incremental at %s" % dt)
#
#res2 = scipy.optimize.minimize(
#    objective,
#    numpy.concatenate((m, numpy.diagonal(c))),
#    args=(comparisons,),
#    options={"ftol":1e-10},
#    bounds=scipy.optimize.Bounds(
#        lb=0,
#        ub=numpy.inf
#    )
#)
#
#dt2 = datetime.datetime.now()
#print("finished incremental at %s" % dt)
#
#print(dt2 - dt)
#
    dt = datetime.datetime.now()
    print("starting full at %s" % dt)

    res2 = scipy.optimize.minimize(
        objective,
        numpy.concatenate((means, numpy.diagonal(cov))),
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
