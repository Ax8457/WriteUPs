# Flag FM challenge WU

<p align="center"><img src="./Screenshots/chall.png"></p>

## Hastad Broadcast attack

$$\begin{cases}
c_1 \equiv m^e \pmod{N_1} \\
c_2 \equiv m^e \pmod{N_2} \\
\vdots \\
c_k \equiv m^e \pmod{N_k}
\end{cases}$$

Which can be also written as:

$$\begin{cases}
m^e \equiv c_1 \pmod{N_1} \\
m^e \equiv c_2 \pmod{N_2} \\
\vdots \\
m^e \equiv c_k \pmod{N_k}
\end{cases}$$

And the Chinese Remainder Theorem can retreive M^e, with

$$C \equiv m^e \pmod{N_{total}}$$

$$N_{total} = \prod_{i=1}^{k} N_i = N_1 \cdot N_2 \cdot \dots \cdot N_k$$

$M_i = \frac{N_{total}}{n_i}$

$$T_i = c_i \cdot M_i \cdot y_i$$

$$m^e = \left( \sum_{i=1}^{k} T_i \right) \pmod{N_{total}}$$

$$m^e = \left( \sum_{i=1}^{k} c_i \cdot M_i \cdot y_i \right) \pmod{N_{total}}$$


## Flag



````bash
python3 hastad.py 

#[+] Starting Håstad's Broadcast Attack
#[+] Opening connection to localhost on port 5003: Done
#[+] Connected to localhost:5003
#[*] Collecting 512 samples...
 #   [PROGRESS] 512/512 collected
#[+] Computing CRT...
#[*] Searching for e and computing e-th root...

#[!!!] SUCCESS! Found e = 317
#[+] Recovered hex: 4612ce170c67e169744f7e3476e69eba3afe864a6548de1a9d661baf3816a6cd038ecf193e5270af048dffc0b570de1663b13b8047af3480491d811307c05b71
#[*] Submitting to original session...

#[SERVER RESPONSE]
#[+] Receiving all data: Done 
#[*] Closed connection to localhost port 5003
#Congratulations! Here is your prize: pwnEd{LOCAL_FLAG_TEST}
````
$$i \approx \frac{512 \times 257}{2048} = \frac{131\,584}{2048} = \mathbf{64,25}$$

````bash
python3 hastad2.py

#[+] Starting Optimized Håstad's Broadcast Attack
#[+] Connected to flag_fm.quals.sigint.mx
#[*] Collecting data and testing roots...
#    [***] Samples: 74/135

#[!] SUCCESS AT 74 SAMPLES!
#[+] Found e = 293

#[FLAG]
#Congratulations! Here is your prize: pwnEd{RSA_15_5up3r_53cur3_ade3f7e3c9dc0973377e8e88f3}
````

FLAG: _pwnEd{RSA_15_5up3r_53cur3_ade3f7e3c9dc0973377e8e88f3}_
