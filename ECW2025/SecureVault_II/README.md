# Crypto - Secure Vault II

<p align="justify">This challenge is linked to <a href="../SecureVault_I/">Secure Vault I</a> challenge which must be completed to solve this one. As a recall, in the first part an encrypton script has been extracted from the memory dump. This script was used to encrypt another PNG file and the goal in this challenge is to break encryption of a PNG by cryptanalyzing the encryption algorithm retreived. </p>

### Encryption mechanism
<p align="justify">Below is the python script used to encrypt the PNG file containing the flag. This script is a simple implementation of AES-GCM encryption mode, which is a stream
cipher based on CTR logic. To make the key more robust agains't guessing attack a SHA3 hash is used to compute the key used for encryption :</p>

````python3
from Crypto.Hash import SHA3_512
from Crypto.Cipher import AES

filename = "0TT4fjq1BN8k.png"

#SHA3-512 so very secure! :)
def very_secure_hash(state):
	h = SHA3_512.new()
	h.update(state)
	return h.digest()[:6]

steps = 306210010937948737844847939557021440793	

state = bytes.fromhex("67342b2ebc70")

for i in range(steps):
	state = very_secure_hash(state)

key = state + state + state[:4]
nonce = bytes.fromhex("cafedecadeadbeef8badf00d000ff1ce")
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
open(filename + ".enc", "wb").write(cipher.encrypt(open(filename, "rb").read()))
````

### Identify the cryptographic flaw in the implementation of the AES-GCM encryption
<p align="justify">To understand how the flag has been encrypted </p>

<p align="center"><img src="Screenshots/S1.png"></p>

$$
Cipher_i = Plaintext_i \oplus E_K(\text{nonce} \| \text{counter})
$$

$$
Plaintext_i = E_K(\\text{nonce} \| \text{counter}) \oplus Cipher_i
$$

$$
Keystream = E_K(\\text{nonce} \| \text{counter}) 
$$

$$
Cipher1 = Keystream \oplus Plaintext1
$$

$$
Cipher2 = Keystream \oplus Plaintext2
$$

$$
\text{Keystream} = \text{Cipher}_1 \oplus \text{Plaintext}_1 \quad \text{and} \quad \text{Keystream} = \text{Cipher}_2 \oplus \text{Plaintext}_2
$$



$$
\iff Cipher1 \oplus Plaintext1  =  Cipher2 \oplus Plaintext2 
$$

$$
\iff Plaintext2  =  Cipher1 \oplus Plaintext1 \oplus Cipher2
$$

### Cycle detection using Brent Algorithm 


FLAG : _ECW{B4d_CrypT0_H4SH_fUncT1on...}_, thanks _Université de Limoges_ for this challenge !

<p align="center"><img src="flag_gcm_7583689.png"></p>
