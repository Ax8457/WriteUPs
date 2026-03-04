# Sony Bologna Challenge WU

<p align="center"><img src="./Screenshots/chall.png"></p>

<p align="justify">In this challenge the idea was to be able to sign a message using elliptic curve signature algorithm ECDSA. The source code was provided and is attached to this repository.</p>

## Source code analysis

## Flag

````bash
python3 ecdsa_exploit.py

#[+] Opening connection to sony_bologna.quals.sigint.mx on port 5000: Done
#[*] Received r and s: r=14468831014805258531945638619826945719876004899592876288452021172713, s1=24365923044581179960849942456501013265368913188341807380080818975757, #s2=2817072497174165802620443728168503651435217382368230041290440823575
#[+] Privkey extracted: dA = 0xe01c14c7b966bd4c6e57a2c358ff680729d288aa8703216eccea879d
#[*] Sending forged signature: r=14468831014805258531945638619826945719876004899592876288452021172713, s=14983007258041658397961331280413012797129933534229001047012713683263
#[+] Receiving all data: Done 
#[*] Closed connection to sony_bologna.quals.sigint.mx port 5000

#pwnEd{m3_wh3n_7h3_ps3_us3s_7h3_s4m3_n0nc3_c62d73caf4a9356bb0205fdc442defa2}
````

FLAG: _pwnEd{m3_wh3n_7h3_ps3_us3s_7h3_s4m3_n0nc3_c62d73caf4a9356bb0205fdc442defa2}_
