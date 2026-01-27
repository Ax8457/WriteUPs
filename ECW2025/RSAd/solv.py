from Crypto.PublicKey import RSA
from sympy import isprime
import base64
import math 
from Crypto.Util.number import long_to_bytes, inverse

public_key = RSA.importKey(open('./pub.key', 'r').read())
n = public_key.n
e = public_key.e

with open('./ciphertext.txt', 'r') as f :
	b64_cipher = f.read()

decoded_bytes = base64.b64decode(b64_cipher)
int_cipher = int.from_bytes(decoded_bytes,byteorder='big')
c = int_cipher 

print(f"e = {e}")
print(f"n = {n}")
print(f"c = {int_cipher}")

#print(math.gcd(e,n))


p1 = 10919940107034605219 
p2 = 16447071910419953861 
p3 = 17241821787594740653 
p4 = 18012762597747138041 
p5 = 66637533603400409223323618618931228858113120065268982016035110037371109083233

l = [p1,p2,p3,p4,p5]
phi_n = 1 
for element in l:
	print(isprime(element))
	phi_n *= (element-1)
	

d = inverse(e,phi_n)
m = pow(c, d, n)
print(long_to_bytes(d))


