# Crypto - RSAd 

<p align="justify"> In this challenge the goal was to retreive the plaintext of the ciphertext encrypted using RSA cryptosystem. To do so only the public key was provided in certificate format.</p>

<p align="justify">Because the public key is provided as a certificate the first step is to extract the public exponent e and the modulus n. Besides, cipher is given as a base64 string, hence it must be extracted properly and converted to n.  The public key (e,N) and cipher text c extraction gives :</p>

````python
e = 498086328087999275701053380915446665606396643116307821653588967790742104960017432814297623619625988464523373061956589449084039484839309959920304533791481
n = 3716988686903660069882200144593397220891733095113506351593605688140148007039485335211705258108910464894219203542907578145260135966195170704004891950321931
c = 477580710635436297929674891793937003080347195674623005134061563261124876153985063982264031046203442652723269417286915502317871230661418818011492102287742
````

### RSA cryptosystem and Euler's Theorem
<p align="justify">Now let's dive into RSA cryptosystem. Below is the Euler totient function with respect to Euler's theorem, on which RSA cryptosystem lies.</p>

<p align="justify"> The prime factorization is given below (each p is prime, alpha is the power of each prime): </p>

$$
n = \prod_{i=1}^k p_i^{a_i}
$$

<p align="justify">Then the Euler Totient function can be computed using:</p>

$$
\phi(n) = n \prod_{i=1}^k \left(1 - \frac{1}{p_i}\right)
$$  

<p align="justify">And below is the relation below public key and private key:</p>

$$
ed \equiv 1 \pmod{\varphi(n)}
$$


<p align="justify">The RSA problem is based on the fact that prime elements of n can't be easyly retreived (namely n can't be factorized and Euler totient retreived). In RSA n must be computed using only two huge prime numbers (k = 2) but what if n is the product of multiple prime numbers ? Then Euler's theorem is still valid and RSA too.

### Solve

<p align="justify">The factorization of n revealed successful and outputed 5 primes numbers :</p>

````python
p1 = 10919940107034605219 
p2 = 16447071910419953861 
p3 = 17241821787594740653 
p4 = 18012762597747138041 
p5 = 66637533603400409223323618618931228858113120065268982016035110037371109083233
````

<p align="justify">It means it's actually possible to retreive totient function and retreive private key to decrypt the message. Since the power of each prime factor is 1, the totient function simplifies to: </p>

$$
\varphi(n) = (p_1 - 1)(p_2 - 1) \cdots (p_k - 1)
$$

<p align="justify">Finally, the private key can be retreived using modular exponentiation inverse : </p>

$$
d \equiv e^{-1} \pmod{\varphi(n)}
$$

<p align="justify">Summary of solv: </p>

*  Extract public key (e,n)
*  Factorize n
*  Compute Euler Totient
*  Compute modular inverse of e to retreive d
*  Decrypt cipher text

<p align="justify"> The script solv.py is attached to this repo and implements each step described above and print the Flag. As a matter of fact the flag int value wasn't the decrypted message but the private key d !</p>

FLAG : _ECW{I_l0ve_rSA_pRiV4t3_K3Y_t00}_ , Thanks _Houko_ for this challenge ! 






