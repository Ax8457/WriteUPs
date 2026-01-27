# The Roughness of Vigenere Challenge WU

<p align="center"><img src="Screenshots/S1.png" style="width: 50%"></p>

<p align="justify">In this crypto challenge, the goal was to retreive the key used to encrypt the plaintext with polyalphabetic algorithm of Vigenere. Only the ciphertext was provided and as a hint, the key was reported to be huge. </p>

## Compute Measure of Roughness for each key size 
<p align="Justify">Given the ciphertext was big enough, it was possible to make a frequency analysis, but it assumes that key length is known. So the first step is to retreive the size of the key, and to
do so the Measure of Roughness can be computed. The logic is the following<:/p>
  
- For each size of key L , the cipher text is divided in L subgroups 
- For each letter of each subgroup, the relative frequency is computed
- For each subgroup the measure of roughness is computed based on the global probs of the ciphertext
- Finally for eahe size of key L, the average measure of roughness is computed and the highest is most likely to be associated to the actual key size

<p align="justify">Below are details of different computation steps :</p>

### 1. Relative frequency per group
<p align="justify">For each subgroup, the relative frequency of each letter is given by: </p>

$$P_{i,j} = \frac{f_{i,j}}{N_i}$$

<p align="justify">Where $$f_{i,j}$$ is the frequency of a letter $${j}$$ in a group $${i}$$ and $${N_i}$$ the number of letters of the subgroup $${i}$$</p>

### 2. Measure of Roughness ($MR$) for group $i$

<p align="justify">Then, based on the computed relative frequency for each subgroup, the associated measure of roughness is given by:</p>

$$MR_i = \sum_{j=0}^{n-1} (P_{i,j} - G_j)^2$$

<p align="justify">Where $${G_j}$$ is the global prob of a letter $${j}$$ in the ciphertext</p>

### 3. Mean Measure of Roughness

<p align="justify">Finally, the mean measure of roughness is computed and the highest $${MR_mean}$$ is the one associated to the right size $${L}$$ of key:</p>

$$\text{Score} = \frac{1}{L} \sum_{i=0}^{L-1} MR_i$$

<p align="justify">The script attached to this repo implements the different steps depicted above and outputs the key size associated to maximum measure of roughness: </p>
  
````bash
python3 mr_solv.py mr_cipher.txt

## With a max key length of 700, if max key length was 100, highest MR would have been 2*372=744
## Max MR = 0.036362 for Key length = 372
````

## Frequency analysis on each subgroup with the right key size
<p align="justify">Once the right size of key is retreived, a classical frequency analysis can be realized on each subgroup and because the ciphertext is long enough, it's very likley to be successful. The script attached to this repo performs the attack based on the key length retreived: </p>

````bash
python3 solv_key.py

##Key retreived (len 372): FGWUIREUYSTZQGHCMILKIPJUYVMEHLRQDKXBOXUDPCTUGAYDDWCDLTKRVJXCQZVVCXGEXIKUORLSGAOHBDSWYYPWGXFGEFTUHJBLWZJDUOSLXERJOBOFJRACQTPEJBQLDFJPJDJTRZMYDRTTMXJOPYLVJYTJKYDJTMYNYMOJAHMQFLILUOFRNWRPCVXHAUEGJNCHNBFPYHGNRLBISOQPUBUEBLPTFSBUOTTEJWWGIWJORTTUOZXOHAJDNPSFUFRESFYVFMXUTPUNYZNSFSUHADZUTIRIGHBCPLQMIDCJNNXFFCXPKGGNGWKYIFOXVZRFYZKDAYGNKSGHACNLERHSFRYXUZQISJJFUPYPKRZADOLNZOTJBXNM
````

## Flag 

````bash
echo -n 'FGWUIREUYSTZQGHCMILKIPJUYVMEHLRQDKXBOXUDPCTUGAYDDWCDLTKRVJXCQZVVCXGEXIKUORLSGAOHBDSWYYPWGXFGEFTUHJBLWZJDUOSLXERJOBOFJRACQTPEJBQLDFJPJDJTRZMYDRTTMXJOPYLVJYTJKYDJTMYNYMOJAHMQFLILUOFRNWRPCVXHAUEGJNCHNBFPYHGNRLBISOQPUBUEBLPTFSBUOTTEJWWGIWJORTTUOZXOHAJDNPSFUFRESFYVFMXUTPUNYZNSFSUHADZUTIRIGHBCPLQMIDCJNNXFFCXPKGGNGWKYIFOXVZRFYZKDAYGNKSGHACNLERHSFRYXUZQISJJFUPYPKRZADOLNZOTJBXNM' | sha256sum

# a3ee1f2b7797cc2aa80a610155868523f6c0202eae82d7e048281891b88d8ff4
````

FLAG: _HACKDAY{a3ee1f2b7797cc2aa80a610155868523f6c0202eae82d7e048281891b88d8ff4}_
