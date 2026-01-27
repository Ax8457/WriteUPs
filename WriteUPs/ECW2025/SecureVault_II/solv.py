from Crypto.Hash import SHA3_512
from Crypto.Cipher import AES
import os

## enc png flag
with open('./flag.png.enc','rb') as f:
    cipher_flag_png = f.read()

print(f"{len(cipher_flag_png.hex())}")

#init plaintext based on the length of the flag
plaintext = bytes([0xAA]) * len(cipher_flag_png)

def xor_blocks(b1: bytes, b2: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(b1, b2))

## target cyclic function
def very_secure_hash(state):
    h = SHA3_512.new()
    h.update(state)
    return h.digest()[:6]

initial_state = bytes.fromhex("67342b2ebc70") # random init state
nonce = bytes.fromhex("cafedecadeadbeef8badf00d000ff1ce")
steps = 7583689 ## modified steps using values retreived from brent alg
state = initial_state
for _ in range(steps):
	state = very_secure_hash(state)	
key = state + state + state[:4]
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
cipher_controlled = cipher.encrypt(plaintext)
keystream = xor_blocks(cipher_controlled, plaintext)
flag_bytes = xor_blocks(keystream, cipher_flag_png)
with open(f"./flag_png/flag_gcm_{steps}.png", "wb") as f:
	f.write(flag_bytes)

#ECW{B4d_CrypT0_H4SH_fUncT1on...}
