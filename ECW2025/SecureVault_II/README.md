# Crypto - Secure Vault II

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



FLAG : _ECW{B4d_CrypT0_H4SH_fUncT1on...}_, thanks _Université de Limoges_ for this challenge !

<p align="center"><img src="flag_gcm_7583689.png"></p>
