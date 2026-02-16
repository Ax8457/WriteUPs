#!/usr/bin/env python3
from Crypto.Hash import SHA3_512
TRUNC_BYTES = 6   	
##target function 
def very_secure_hash(state: bytes) -> bytes:
    h = SHA3_512.new()
    h.update(state)
    return h.digest()[:TRUNC_BYTES]
    
## source : https://en.wikipedia.org/wiki/Cycle_detection#Brent's_algorithm
## https://en.wikipedia.org/wiki/Cycle_detection
def brent(f, x0) -> (int, int):
    """Brent's cycle detection algorithm."""
    # main phase: search successive powers of two
    power = lam = 1
    tortoise = x0
    hare = f(x0)  # f(x0) is the element/node next to x0.
    # this assumes there is a cycle; otherwise this loop won't terminate
    while tortoise != hare:
        if power == lam:  # time to start a new power of two?
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1

    # Find the position of the first repetition of length λ
    tortoise = hare = x0
    for i in range(lam):
        hare = f(hare)
    # The distance between the hare and tortoise is now λ.

    # Next, the hare and tortoise move at same speed until they agree
    mu = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
 
    return lam, mu

x0 = bytes.fromhex("67342b2ebc70")
lam,mu = brent(very_secure_hash,x0)
print(f"lam: {lam}")
print(f"mu: {mu}")

### lam: 5779304
### mu: 6984369
