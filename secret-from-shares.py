import json
from ffield import FField, FFieldElement as FFElem

ffield = FField(11953696440786470837)

def submatrix(i, j, A):
    return [
        [A[x][y] for y in xrange(len(A[x])) if y != j]
            for x in xrange(len(A)) if x != i
    ]

def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]

def det3(A):
    det = reduce(
        (lambda x, y: x + y),
        [A[0][i] * det2(submatrix(0, i, A)) for i in xrange(len(A))]
    )
    return det

def dot(a, b):
    return reduce(
        (lambda x, y: x + y), 
        [a[i] * b[i] for i in xrange(len(a))]
    )

def column(j, A):
    return [A[i][j] for i in xrange(len(A))]

def minors(A):
    minors = [
        [det2(submatrix(i, j, A)) for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    return minors

def cofactors(A):
    cofactors = [
        [A[i][j] * ((-1) ** (i + j)) for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    return cofactors

def transpose(A):
    transpose = [
        [A[j][i] for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    return transpose

def main():
    secrets = json.load(open('local-shares.json', 'r'))
    shares = secrets[1]
    for i in xrange(len(shares)):
        shares[i][0] = FFElem(ffield, shares[i][0])
        shares[i][1] = FFElem(ffield, shares[i][1])
    A = [
        [(shares[i][0] ** (j + 1)) for j in xrange(len(shares))]
            for i in xrange(len(shares))
    ]
    b_transpose = [shares[i][1] for i in xrange(len(shares))]

    # Invert A
    A_minors = minors(A)
    A_cofactors = cofactors(A_minors)
    A_transpose = transpose(A_cofactors)
    det = det3(A)
    inverse = [
        [A_transpose[i][j] / det for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    identity = [
        [dot(inverse[i], column(j, A)) for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    assert identity[0][0].value == identity[1][1].value
    assert identity[1][1].value == identity[2][2].value
    # some weird stuff happens where my inverse is off by a scalar multiple...
    # something to do with multiplicative inverse mod p
    scalar = identity[0][0]
    det *= scalar
    inverse = [
        [A_transpose[i][j] / det for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    identity = [
        [dot(inverse[i], column(j, A)) for j in xrange(len(A[i]))]
            for i in xrange(len(A))
    ]
    assert identity[0][0].value == identity[1][1].value
    assert identity[1][1].value == identity[2][2].value
    assert identity[0][0].value == 1


    # the solution vector is A_inverse * b
    s = [dot(inverse[i], b_transpose) for i in xrange(len(A))]

    # make sure that this really is a solution
    b_soln = [dot(A[i], s) for i in xrange(len(A))] 
    for i in xrange(len(b_transpose)):
        assert b_soln[i].value == b_transpose[i].value
    print "Solution vector:", s
    print "Secret:", s[0]
    

if __name__ == "__main__":
    main()
