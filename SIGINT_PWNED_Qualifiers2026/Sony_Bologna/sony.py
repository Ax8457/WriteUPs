#!/usr/local/bin/python3

import os

from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, getRandomInteger
from ecutils.core import EllipticCurve, Point

def leftmost_n_bits(e, n):
    bitlen = e.bit_length()
    if n >= bitlen:
        return e
    return e >> (bitlen - n)

def sign_message(m: bytes, dA: int, curve: EllipticCurve, k: int|None = None):
    e = bytes_to_long(SHA256.new(data=m).digest())
    z = leftmost_n_bits(e, curve.n.bit_length())
    if not k:
        k = getRandomInteger(curve.n.bit_length())
    X = curve.multiply_point(k, curve.G)
    r = X.x % curve.n
    if r == 0:
        return sign_message(m, dA)
    s = (pow(k, -1, curve.n) * (z + r * dA)) % curve.n
    if s == 0:
        return sign_message(m, dA)
    return (r, s)

def verify_signature(m: bytes, r: int, s: int, QA: Point, curve: EllipticCurve) -> bool:
    if not (1 < r < curve.n-1 and 1 < s < curve.n-1):
        return False
    e = bytes_to_long(SHA256.new(data=m).digest())
    z = leftmost_n_bits(e, curve.n.bit_length())
    u1, u2 = (z*pow(s, -1, curve.n) % curve.n), (r*pow(s, -1, curve.n) % curve.n)
    X = curve.add_points(curve.multiply_point(u1, curve.G), curve.multiply_point(u2, QA))
    if (X.x % curve.n) == r:
        return True
    return False

def main():
    curve = EllipticCurve(p=0xffffffffffffffffffffffffffffffff000000000000000000000001,
                          a=0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe,
                          b=0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4,
                          G=Point(0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21,
                                   0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34),
                          n=0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d,
                          h=0x1)
    dA, k = getRandomInteger(curve.n.bit_length()), getRandomInteger(curve.n.bit_length())
    QA = curve.multiply_point(dA, curve.G)

    r, s1 = sign_message(b"I'm a cat!", dA, curve, k=k)
    r, s2 = sign_message(b"Wuff! Wuff!", dA, curve, k=k)
    print(f"{r=}\n{s1=}\n{s2=}")

    try:
        gr, gs, = int(input("r: ")), int(input("s: "))
    except ValueError:
        print("You must enter valid base 10 integers.")
        return
    if verify_signature(b"g1v3_m3_7h3_fl4g", gr, gs, QA, curve):
        print(os.environ["FLAG"] if os.environ.get("FLAG") else "pwnEd{TEST_FLAG}")
    else:
        print("Something doesn't seem right here... No flag for you!")

if __name__ == "__main__":
    main()
