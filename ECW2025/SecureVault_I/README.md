# Forensics - Secure Vault I

<p align="justify"></p>

````bash
python3 vol.py -f image.raw windows.cmdline | grep "encrypt"

#3444	py.exe	py.exe  encrypt.py
#4936	python.exe	C:\Users\crypto\AppData\Local\Programs\Python\Python313\python.exe  encrypt.py
````
````bash
python3 vol.py -f image.raw windows.filescan | grep "encrypt"
#0xbd06170982c0 \Users\crypto\Desktop\encrypt.py
#0xbd0619646930	\Users\crypto\AppData\Roaming\Microsoft\Windows\Recent\encrypt.lnk
#0xbd061965fc50	\Users\crypto\Desktop\encrypt.py
````

````bash
python3 vol.py -f image.raw windows.dumpfiles --virtaddr 0xbd061965fc50 
````

```python3
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

````bash
python3 vol.py -f image.raw windows.filescan | grep "0TT4fjq1BN8k.png"
````

