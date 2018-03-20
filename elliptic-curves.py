from ffield import FField, FFieldElement as FFElem

p = 2017
field = FField(p)
A = FFElem(field, 5.)
B = FFElem(field, 3.)


def add(P, Q):
    if P[0] == Q[0] and P[1] == Q[1]:
        lamb = (FFElem(field, 3) * P[0] ** 2 + A) / (FFElem(field, 2) * P[1])
    else:
        lamb = (Q[1] - P[1]) / (Q[0] - P[0])
    x = lamb ** 2 - P[0] - Q[0]
    y = lamb * (P[0] - x) - P[1]
    # assert point is on curve
    S = (x, y)
    assert S[1] ** 2 - (S[0] ** 3 + A * S[0] + B) <= 0.0001
    return S


def mult(n, P):
    assert n > 0
    S = P
    for i in xrange(n - 1):
        S = add(P, S)
    # assert point is on curve
    assert S[1] ** 2 - (S[0] ** 3 + A * S[0] + B) <= 0.0001
    return S


# calculate P + Q
def calcb1():
    P = (FFElem(field, 60.), FFElem(field, 22.))
    Q = (FFElem(field, 13.), FFElem(field, 128.))
    S = add(P, Q)
    print "P + Q is", S


# calculate 100G
def calcb2():
    G = (FFElem(field, 292.), FFElem(field, 374.))
    S = mult(100, G)
    print "100G is", S


def calcc():
    G = (FFElem(field, 292.), FFElem(field, 374.))
    S_a = 21
    S_b = 35
    P_a = mult(S_a, G)
    P_b = mult(S_b, G)

    print "Alice sends", P_a
    print "Bob sends", P_b
    secret_a = mult(S_a, P_b)
    secret_b = mult(S_b, P_a)
    assert secret_a[0] - secret_b[0] <= 0.0001
    assert secret_a[1] - secret_b[1] <= 0.0001
    print "Shared secret point is", secret_a
    print "Shared secret is", secret_a[0]


def main():
    print "3-1 (b)"
    calcb1()
    calcb2()

    print "\n3-1 (c)"
    calcc()


if __name__ == "__main__":
    main()
