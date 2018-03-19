from os import urandom


def xgcd(a, b):
    # Return (g, x, y) such that ax + by = g = gcd(a, b)
    prevx, x, prevy, y = 1, 0, 0, 1
    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b
    return a, prevx, prevy


class FField:
    # GF(p)
    def __init__(self, module):
        self.module = module

    def __repr__(self):
        return 'GF(%d)' % self.module

    def randomElement(self):
        l = self.module.bit_length()
        r = self.module
        while r >= self.module:
            r = int(urandom((l + 7) / 8).encode('hex'), 16)
            r &= (1 << l) - 1
        return FFieldElement(self, r)


class FFieldElement:
    # GF(p) element
    def __init__(self, ffield, value):
        self.ffield = ffield
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __pow__(self, pow):
        return FFieldElement(
            self.ffield,
            (self.value ** pow) % self.ffield.module
        )

    def __add__(self, another):
        if isinstance(another, FFieldElement):
            assert self.ffield == another.ffield
            other_val = another.value
        else:
            other_val = another
        return FFieldElement(
            self.ffield,
            (self.value + other_val) % self.ffield.module
        )

    def __sub__(self, another):
        if isinstance(another, FFieldElement):
            assert self.ffield == another.ffield
            other_val = another.value
        else:
            other_val = another
        return FFieldElement(
            self.ffield,
            (self.value - other_val) % self.ffield.module
        )

    def __mul__(self, another):
        if isinstance(another, FFieldElement):
            assert self.ffield == another.ffield
            other_val = another.value
        else:
            other_val = another
        return FFieldElement(
            self.ffield,
            (self.value * other_val) % self.ffield.module
        )

    def __div__(self, another):
        if isinstance(another, FFieldElement):
            assert self.ffield == another.ffield
            other_val = another.value
        else:
            other_val = another
        assert other_val != 0
        _, x, _ = xgcd(other_val, self.ffield.module)
        return FFieldElement(
            self.ffield,
            (self.value * x) % self.ffield.module
        )
