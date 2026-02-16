# Secure Login Challenge WU

<p align="center"><img src="./Screenshots/chall.png"></p>

<p align="justify">In this challenge the idea was to retreive prime integers $p$ and $q$ used to compute ssh format RSA keys and to use it to connect to a server.To do so, the script used to generate keys was provided and is attached to this repository :</p>

````python
from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime
from sympy import nextprime

p = getPrime(2048)
q = nextprime(p)
e = 0x10001

key = RSA.construct((p*q, e))
pem = key.export_key(format="PEM")
with open("public_key.pem", "wb") as f:
    f.write(pem)
````
