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
