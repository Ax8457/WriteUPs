# Forensics - Secure Vault I

<p align="justify">In this challenge the goal was to retreive a file before he was encrypted, working on a raw memory dump. Looking at first hundreds of raw data file, it indicates that it must be a dump of a windows machine, hosted on a VirtualBox hypervisor.</p>

<p align="center"><img src="Screenshots/S.png" style="width:50%"></p>

### Forensics analysis using volatility3 

<p align="justify">Keeping in mind that we must retreive a file before he was encrypted, it means the file is very likely to be present on the machine and/or opened by a process such as notepad, notepad++ or other editor tool. Volatility provides multiples plugins to analyze a windows machine raw memory dump and retreive this kind of information: </p>

* _windows.filscan_ : this plugin prints all files on the host machine when it was dumped, as well as the virtual memory address.
* _windiows.cmdline_ : this plugin prints the cmdline content used to launch process.
* _windows.dumpfiles_ : this plugin dumps files in memory, based on virtual address printed by plugins like _filescan_.
 
### Solv

<p align="justify">To solv this challenge, let's start by looking at cmdline. The idea is to retreive evidences about file encryption (like encryption script, encrypted or unencrypted files, process ...). Grepping the cmdline plugin output reveals a promising python script launched:</p>
	
````bash
python3 vol.py -f image.raw windows.cmdline | grep "encrypt"

#3444	py.exe	py.exe  encrypt.py
#4936	python.exe	C:\Users\crypto\AppData\Local\Programs\Python\Python313\python.exe  encrypt.py
````

<p align="justify"> This python script file is very likely to perform encryption tasks. Using filescan plugin, it's possible to extract its virtual memory address and dump it from the raw memory of the machine.</p>

````bash
python3 vol.py -f image.raw windows.filescan | grep "encrypt"
#0xbd06170982c0 \Users\crypto\Desktop\encrypt.py
#0xbd0619646930	\Users\crypto\AppData\Roaming\Microsoft\Windows\Recent\encrypt.lnk
#0xbd061965fc50	\Users\crypto\Desktop\encrypt.py

python3 vol.py -f image.raw windows.dumpfiles --virtaddr 0xbd061965fc50 
````

<p align="justify"> Based on the content of the script extracted, it seems that it is indeed the script used to encrypt target file we must retreive. This script implements a AES GCM algorithm to encrypt a png file named 0TT4fjq1BN8k.png:</p>

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
<p align="justify"> To get the flag, the last step is to dump this PNG file, using the same method used to dump encryption script (namely extract virtual address wwith filescan and use dumpfile to extract it from memory).</p>

````bash
python3 vol.py -f image.raw windows.filescan | grep "0TT4fjq1BN8k.png"

#0xbd0616e80d20 \Users\crypto\Desktop\0TT4fjq1BN8k.png
#0xbd0618b728f0	\Users\crypto\Desktop\0TT4fjq1BN8k.png

python3 vol.py -f image.raw windows.dumpfiles --virtaddr 0xbd0618b728f0
````

FLAG : _ECW{F0renS1c_is_s0_Much_fUn!!!}_ , thanks _Université de Limoges_ for this chall !

<p align="center"><img src="known_flag.png"></p>

