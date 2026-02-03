# Back To Super Increasing Era Challenge WU

<p align="center"><img src="Screenshots/challBTSE.png" style="width: 50%"></p>

<p align="justify">In this challenge, the goal was to decrypt the cipher text attached.No sources were provided. It seems that the flag was splitted into eight parts of 64 bits each, below is an example:</p>

````txt
{'Cipher': 567895815774543185792374712785597869331, 'MessageSizeBits': 64, 'PublicKey': ['afd1cca0ebf62687a3c65e530fa1e31', 'c9d0d3ebf8daebfbe7e8f7b94eb1aaa', '12c969e5724e30146fb118af53094997', '20fea1417f131e09e1d920e48c247e9b', '15c4817731d5ef0179408a681121d968', '1c897b543f13b325c46b3e36528dffea', '263f96c85a2be8e6e239162ef457215', '248bd0528e39164c9d6c68583b129659', '102d708dd56f32487414608dcc95733a', 'c1c7114e5cbcb848670b266657eaa39', 'a07c7da5dea0ca041a43906090616e2', '62de865004b255e303a8fba272ee4af', '20681edea83fb2118cc45086931c6818', '88f3bd7b41093fa50829106aef5f4fa', '202e95ebac017127619c5b1950f26041', '17eccb5974bdfcff0baf0b039ff78f3', '10d679c961c226d4d5199c237abfedd0', '38801dff4d061a3e1e9e3f09656519e', '1c9788b2ecf7bd9e1574735793e488eb', '22549fd19141e47f8df08d782a62a3e3', '4cbaad139122e89c303882a9dd62014', '18866d0a213980555f60fcefbe67d23b', '11a7f44d2722fb6695b1358ab6a5c1aa', 'eb4b031f7edc18c760f75ca19db1cb6', '694d14f58018f3ae573e58ab70b95c9', '4a76b68c37c04c9e87326bb775e930c', 'e222b7972cb9509823a7f126fc41d46', '41af448573bc4c5407884c45fb8c1f3', '1924bb420877a3f069d8075a48fa055c', '1adc8322488f37898c94d49b4f213ee3', '1ab7ca80b8ebcb975fdc5c242ff555c2', '199fa8c6e1a36d86aa993f4dfb78f094', '8c9e2c2928a11dcfc38182808cef47f', '128c2bcdbbcc0c51df2cd58a25b4fd83', '21e9a02136bb66b10e2086762d1fc94d', '164d6665fad2b76087d1fa522165bcd0', '1fa7f92237bee4989c3ab635fff46516', '1d6d79b088b844d02b1ecf13de5977f1', '1d78001c738f91a6fcd75ff65c6e61c7', '1451efdf149576cb75eb0e8f6af5c142', '66b5fbaf263be9f2a3773359418db08', '345f7be0046a7cf820728b3f60f718c', '1dd57ee379d0c71a305857eec989f644', '3bd866909e3acaa772090677c40af7a', 'dc0851e6cafc0fdfbfaea86b91a43a0', '10f6a355c4340e9de93036049d2737cb', '11c91f4df798483576305cce94378114', 'c0ca62e2b42c04de14dbfb9732be6a9', 'dbfb5140503b0f42bb40081575cdfbd', '183f793ba1861c1fb73ed3289ce79c10', '513eb73a1af81cd052eecd09a9a8128', '4c6297fcb1a66ecdd7ab63a9f360b12', '22b4646c67fff5172ed66966dd33138c', '3a653e964a069f4ca8015c12e9a7160', '9d6aed40f6309ecb05930b342a2457f', '12e5b8ff62ef5c4c0adb82d4cc46062e', '1f5a106b7fb9394d02d5eff72b74d457', '12dd3da1a011fd0a683e147146a2e030', '17aac2374df63d820e1d649d225763c7', '35b8bb61661f3068b239892935287a7', '19948264beedd5af46adbf60a21472a', '8756e0410154f90d01b7acb1801f5f8', '2240ce2c3ca4d64203b014db8bc7d85c', '218e0f2fbc2544cba6ef5987ff1c0d70']}
````
<p align="justify">The structure of the public key suggests that the cryptosystem used must be based on a super increasing sequence, because each of the 64 bits of the message has its public key comonent associated. Hence, this cipher must have been encrypted using Merkle Hellman cryptosystem, insofar as it is the only reportedly breakable. </p>
  
## Merkle Hellman Cryptosystem

### Key generation
<p align=justify">The Mekle Hellman cryptosystem is based on a super increasing sequence which serves as the private key (with $q$ and $w$).Let's say that message is of size $n$ (in bits), the sequence is generated with respect to following properties:</p>

$$e_i > \sum_{k=1}^{i-1} e_k$$

<p align=justify">The public key is then computed using the following modular arithmetic logic : 

$$h_i = (w \cdot e_i) \pmod{q}$$ 

<p align=justify">with $gcd(w, q) = 1$ and $$q > \sum_{i=1}^{n} e_i$$ (to avoid wrap-around and data loss) </p>

### Encryption

<p align=justify">The encryption if performed by the following sum, wich actually 'selects' elements of the public key to add to the cipher (because bits of the message are 0 or 1):</p>

$$C = \sum_{i=1}^{n} (b_i \cdot h_i) = \sum_{i=1}^n (b_i\cdot e_i\cdot w\pmod q)$$

### Decryption

<p align=justify">For the decryption, the first step of the decryption process consists of neutralizing the weight transformation by multiplying the ciphertext $C$ by the modular inverse of the multiplier $w$:</p>

$$C' = C \cdot w^{-1} \equiv \left( \sum_{i=1}^{n} a_i \cdot w \cdot e_i \right) \cdot w^{-1} \pmod q$$

$$C' = \sum_{i=1}^{n} (b_i \cdot e_i)$$

<p align=justify">The result can be written as:</p>

$$C' = \sum_{i=1}^{n} b_i e_i = \left( \sum_{i=1}^{n-1} b_i e_i \right) + b_n e_n$$

<p align=justify"> And because $$e_i > \sum_{k=1}^{i-1} e_k$$ even if all the message bits are equal to 1 we have $$e_n > \sum_{k=1}^{n-1} e_k b_k$$ and the only condition to get  $$C' \geq e_n$$ is:</p>

$$b_n = 1 \iff C' \geq e_n$$ 

<p align=justify">Finally the decryption follow the logic below: </p>

$$
b_n = \begin{cases} 
1 & \text{if } C' \geq e_n \\ 
0 & \text{if } C' < e_n 
\end{cases}
$$

<p align=justify">And if the bit $i$ is 1, $C'$ is decremented by the element $e_i$ :</p>

$$C'_{i-1} = C_i' - e_i$$

## Breaking the cipher:  Lattice Reduction

<p align="justify">Merkle Hellman was actually reported as unsafe, because of the fact that it lies on knapsack problem, which is vulnerable to lattice reduction attack. If the density of the knapsack is under 0.9408, it means that the cipher can be broken because of a weak super increasing sequence. The density is computed by: </p>
  
$$d = \frac{n}{\log_2(\max(Pubkey_i))}$$

<p align="justify">Running the script density.py attached to this repo reveals that both public keys used for encryption of each of the 8 parts of the flag are vulnerable to lattice reduction with densities around 0.5:</p>

````bash
 python3 density.py

##   | n (bits) | Max Value (bits)   | Density    | Vulnerability
#---------------------------------------------------------------------------
#0   | 64       | 125.19             | 0.511216   | VULNERABLE
#1   | 64       | 124.27             | 0.515021   | VULNERABLE
#2   | 64       | 126.37             | 0.50643    | VULNERABLE
#3   | 64       | 123.08             | 0.520006   | VULNERABLE
#4   | 64       | 126.48             | 0.506007   | VULNERABLE
#5   | 64       | 124.46             | 0.514209   | VULNERABLE
#6   | 64       | 125.4              | 0.51036    | VULNERABLE
#7   | 64       | 126.91             | 0.504313   | VULNERABLE

````

<p align="justify">But how the lattice reduction works on Merkle Hellman? This is perfeclty explained is this <a href="https://www.cs.sjsu.edu/faculty/stamp/papers/topics/topic16/Knapsack.pdf">paper</a>. Lattice reduction transforms a math problem (here how to find a vector U with the bits of the encrypted message) into a geometrical problem (basically find the shortest vector U in a matrix) thanks to Lattice networks. The scripts attached to this repo implements the Lattice reduction on each of the ciphertexts and must be run with sage (on <a href="https://cocalc.com/features/sage">cocalc</a>) The idea is to find a vector shortest U so that:</p>

$$[b_0, b_1, \dots, b_{n-1}] \times \begin{bmatrix} u_0 \\ u_1 \\ \vdots \\ u_{n-1} \end{bmatrix} = [C]$$

## Script details

<p align="justify">The script solv.py attached to this repo implements a knapsack lattice reduction:</p>
  
- The solution script uses a CJM marix with a BKZ reduction method to find the shortest vector (Shortest Vector Problem)
- The section below aims to solve the problem of negative vector found, indeed mathematically speaking $-W$ is as short as $W$ (because of the way the norm is computed)

````python
         #Reverted Bits
            alt_bits = [1-b for b in potential_bits] # if b = 1 hence 0 if b = 0 hence 1
            if sum(h * b for h, b in zip(H, alt_bits)) == cipher:
                bit_str = "".join(map(str, alt_bits))
                val = int(bit_str, 2)
                res = val.to_bytes((n // 8), 'big').decode(errors='ignore')
                return res
````
- Weight W is used to automatically exclude the right colum at reduction
- The Matrix CJM with BKZ reduction looks for and outputs a vector with 1 and -1, hence those bits must be substituted with 0 and 1 


## Flag

<p> Running the script attached as solv.py on a sage maths online compiler, it finally outputs: </p>

````txt
[+] Processing ...
Bloc 1: HACKDAY{
Bloc 2: M3rkl3_H
Bloc 3: 3llm4n_c
Bloc 4: rypt0sys
Bloc 5: t3m_l4tt
Bloc 6: 1c3_r3du
Bloc 7: ct10n_4t
Bloc 8: t4ck_!!}
````

FLAG: _HACKDAY{M3rkl3_H3llm4n_crypt0syst3m_l4tt1c3_r3duct10n_4tt4ck_!!_}_
