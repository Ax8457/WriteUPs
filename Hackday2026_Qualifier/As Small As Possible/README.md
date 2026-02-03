# As Small As Possible Challenge WU

<p align="center"><img src="Screenshots/ASAP.png" style="width: 50%"></p>

<p align="justify">In this challenge a Diffie Hellman key exchange with AES GCM encryption Orcale was depoyed, in which it was possible to receive a message from Alice and to send a message to Bob. Based on diffie Hellman, each operation required user to send his public key. The goal was to decrypt the packet exchanged between Alice and Bob below: </p>


````txt
=== TRAFFIC INTERCEPTED ===
Payload: {"iv": "784222c11c46dc7c0383c780", "ciphertext": "8220bdb8b7759632a1109840a99e371e85b522fff957c98c0f66e7806854383c954bd462afc2046f1fa1dd5046ee83134376dd8e7b7c1d3740f93b2020bf731c85", "tag": "177d5ab63b376cdf620d24042f5b7ace"}
===========================
````
<p align="justify">Once the shared secret is computed, on each side messages were encrypted using following function (not exactly HKDF but a simplified version of the key derivation): </p>
    
````python
def encrypt_payload(message, secret):
    key = hashlib.sha256(str(secret).encode()).digest()
    iv = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return {"iv": iv.hex(), "ciphertext": ciphertext.hex(), "tag": tag.hex()}
````

<p align="justify">Because no check was made on the public key submitted if the prime used in unsafe (namely $p-1$ can ba factorized), hence this oracle mights be vulnerable to small subgroups attack.</p>

## Diffie Hellman Key exchange

<p align="justify">Diffie Hellman key exchange algorithm lies on multiplicative group genrated by a integer $g$ called the generator and a prime $p$, shared amoung Alice & Bob. If Alice & Bob want to share public keys, they must follow steps bellow: </p>

- Alice generates a private key $a$ and computes her public key $A=g^a \mod{p}$
- Bob generates a private key $b$ and computed his public key $A=g^b \mod{p}$
- Alice and Bob share their public key
- Alice computes the shared secret $S=B^a \mod{p}$
- Bob computes the shared secret $S=A^b \mod{p}$
  
<p align="justify">Finally Bob and Alice end with the same shared secret they can use to derivate the same symmetric key for encryption using AES GCM:</p>

$$S = (g^b)^a \equiv g^{ba} \equiv g^{ab} \equiv (g^a)^b \pmod{p}$$

<p align="justify">As a matter of fact, the Diffie Hellman group is of order $p-1$ and if the public key accepted isn't checked (and if the number $p-1$ can be factorized), it makes this implementation vulnerable because order of the group can be reduced. With such an attack, Alice secret can be retreived and an attacker could compute the shared secret on his side to decrypt intercepted communication.</p>
    
## Small Subgroups Attack on Diffie Hellman Key exchange

### First Step: p factorization

<p align="justify">The first step is to check if $p$ is unsafe, namely check if $p-1$ can be factorized. $p$ factors are essential as the exploit require integers only.<a href="https://www.dcode.fr/prime-factors-decomposition">This online tool</a> outputs the following factors, confirming that the prime used is unsafe:</p>

````python
factors= [2, 3, 23, 107, 113, 127, 131, 149, 151, 157, 167, 193, 229, 241, 257, 263, 311, 317, 359, 409, 421, 443, 457, 463, 467, 571, 587, 593, 653, 661, 677, 709, 739, 743, 751, 773, 829, 857, 863, 887, 907, 911, 977, 1009, 1033, 1039, 1129, 1151, 1163, 1181, 1229, 1279, 1289, 1307, 1319, 1327, 1367, 1373, 1423, 1447, 1451, 1511, 1523, 1553, 1571, 1579, 1613, 1619, 1637, 1657, 1667, 1669, 1697, 1699, 1709, 1741, 1747, 1777, 1861, 1871, 1879, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1997, 1999, 2017, 2029, 2039, 2063, 2089, 2099, 2131, 2141, 2143, 2161, 2179, 2267, 2273, 2287, 2293, 2333, 2339, 2351, 2357, 2371, 2383, 2393, 2423, 2447, 2459, 2467, 2473, 2521, 2543, 2549, 2557, 2593, 2617, 2659, 2663, 2683, 2741, 2753, 2953, 2957, 2963, 3019, 3061, 3067, 3169, 3181, 3187, 3221, 3271, 3307, 3329, 3347, 3373, 3389, 3391, 3467, 3499, 3527, 3583, 3617, 3623, 3631, 3637, 3677, 3709, 3761, 3769, 3917, 3931, 3943, 4013, 4091, 4127, 4157, 4159, 4201, 4211, 4217, 4327, 4349, 4397, 4493, 4513, 4523, 4547, 4567, 4621, 4637, 4663, 4679, 4721, 4729, 4861, 4871, 4877, 4931, 4937, 4957, 4969, 4993, 7951, 308117]
````

> The multiplicative group is defined on $\mathbb{Z}/p\mathbb{Z}^*$, 0 being excluded because he doesn't have modular inverse, this is why this is $p-1$ which is factorized

### Small subgroups attack

<p align="justify">Now that factors have been extracted, it's possible to retreive Alice private key (namely $a$) by sending specific public keys crafted with each of the factors.It aims to reduce the order of the group and making $a$ easier to recover/guess. The maths behind the attack are explained below:</p>

<p align="justify">As a recall p has been factorized and can be written as the product of each factors:</p>

$$p - 1 = \prod_{i=1}^{k} q_i^{e_i} = q_1^{e_1} \cdot q_2^{e_2} \dots q_k^{e_k}$$

<p align="justify">Then the attacker opens a communication with Alice, and instead of sending a real public key the attacker sends the following key :</p>
    
$$g_i = g^{(p-1)/q_i} \pmod p$$

<p align="justify">It points out why $p-1$ has to be factorized. Because we work only with intergers; $\frac{p-1}{q_i}$ must be an integer otherwise the attack would fail. Once this public key is sent to Alice, she can use it to compute the shared secret and then encrypt a message with the derivated key. Below is the shared secret that Alice computes, with order is reduced to $q_i$:</p>
    
$$S_{Alice} = \left(g^{\frac{p-1}{q_i}}\right)^a \pmod p$$

<p align="justify">Considering that $a$ can be written as :</p>

$$a = k \cdot q_i + r$$

<p align="justify">Following transformation can be made on Alice computed shared secret:</p>

$$S_{Alice} = (g_i)^a \pmod p$$

$$S_{Alice} = (g^{\frac{p-1}{q_i}})^{(k \cdot q_i + r)} \pmod p$$

<p align="justify">Injecting $a$:</p>

$$S_{Alice} = g^{(\frac{p-1}{q_i} \cdot k \cdot q_i)} \cdot g^{(\frac{p-1}{q_i} \cdot r)} \pmod p$$

$$S_{Alice} = g^{(p-1) \cdot k} \cdot g^{\frac{p-1}{q_i} \cdot r} \pmod p$$

$$S_{Alice} = (g^{p-1})^k \cdot (g_i)^r \pmod p$$

<p align="justify">And with respect to <a href="https://en.wikipedia.org/wiki/Fermat's_little_theorem">Little Fermat's Theorem</a>, it can be simplified to:</p>

$$S_{Alice} = (1)^k \cdot (g_i)^r \pmod p$$

$$S_{Alice} \equiv (g_i)^r \pmod p$$

<p align="justify">Since $r$ is constrained to the range $[0, q_i)$, it provides only a partial leak of the private key (order of $q_i$). However, by observing that $a \equiv r \pmod{q_i}$, we can collect several such residues and use the <a href="https://en.wikipedia.org/wiki/Chinese_remainder_theorem">Chinese Remainder Theorem (CRT)</a> to fully reconstruct the secret $a$. The bigger $q_i$ is, and the bigger $r$ is.</p>

$$\begin{cases} 
a \equiv r_1 \pmod{q_1} \\
a \equiv r_2 \pmod{q_2} \\
\vdots \\
a \equiv r_n \pmod{q_n}
\end{cases}$$



### Retreive Alice's key and compute shared secret Between Alice and Bob
<p align="justify">Considering properties above, the attack must follow those steps:</p>

- for each factor $q_i$ the attacker forges a public key $g_i = g^{(p-1)/q_i} \pmod p$
- The attacker sends this public key to Alice, who computes a secret, derivates a symmetric key and uses it to encrypt a message
- The attacker receives the cipher and iterates from 0 to $q_i$, computes $S_{Alice} \equiv (g_i)^r \pmod p$, derivates the symmetric key associated and checks the tag. If the GCM tag is valid, the attacker stores the remainder $r_i$ and the moduli $q_i$
- Once enough information about Alice's private key is collected, the CRT is applied and $a$ is retreived
- The attacker asks bob for his public key, compute the shared Secret $B^a$
- The attacker derives the key and decrypts the flag  


## Flag 

<p align="justify">The script attached to this repo implements the attack and finally outputs: </p>
    
````bash
python3 small_exploit.py

#[*] Analyzing traffic...
#[+] Opening connection to localhost on port 4444: Done
#[*] Closed connection to localhost port 4444
#[*] Starting subgroup injection...
#[+] Opening connection to localhost on port 4444: Done
#[*] Closed connection to localhost port 4444
#[+] Found mod    2 | Bits:  1.0/1024

#***

#[+] Opening connection to localhost on port 4444: Done
#[*] Closed connection to localhost port 4444
#[+] Found mod 2333 | Bits: 1027.7/1024
#[!] Threshold reached. Ready for CRT.

#[*] Reconstructing Alice's Private Key...

#[!] SUCCESS: SECRET_FLAG: Hackday{D1ff13_H3llm4n_Sm4ll_Subgr0ups_4tt4ck_$$$!!}
````

FLAG: _Hackday{D1ff13_H3llm4n_Sm4ll_Subgr0ups_4tt4ck_$$$!!}_
