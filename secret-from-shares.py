import numpy as np
import json
from ffield import FField, FFieldElement as FFElem

ffield = FField(11953696440786470837)

def main():
    secrets = json.load(open('local-shares.json', 'r'))
    shares = secrets[1]
    for i in xrange(len(shares)):
        shares[i][0] = FFElem(ffield, shares[i][0])
        shares[i][0] = FFElem(ffield, shares[i][1])
    A = np.array([
        [shares[0][0], shares[0][0] ** 2, shares[0][0] ** 3],
        [shares[1][0], shares[1][0] ** 2, shares[1][0] ** 3],
        [shares[2][0], shares[2][0] ** 2, shares[2][0] ** 3],
    ])
    b = np.array([shares[0][1], shares[1][1], shares[2][1]])
    s = np.linalg.solve(A, b)
    print "secret: ", s[0]
    print s

if __name__ == "__main__":
    main()
