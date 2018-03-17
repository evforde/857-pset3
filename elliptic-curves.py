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
    return (x, y)


# calculate P + Q
def calc1():
    P = (FFElem(field, 60.), FFElem(field, 22.))
    Q = (FFElem(field, 13.), FFElem(field, 128.))
    S = add(P, Q)
    assert S[1] ** 2 - (S[0] ** 3 + A * S[0] + B) <= 0.1
    print "P + Q is", S


# calculate 100G
def calc2():
    G = (FFElem(field, 292.), FFElem(field, 374.))
    S = G
    for i in xrange(100):
        S = add(G, S)
    assert S[1] ** 2 - (S[0] ** 3 + A * S[0] + B) <= 0.1
    print "100G is", S


def main():
    print "3-1 (b)"
    calc1()
    calc2()


if __name__ == "__main__":
    main()
