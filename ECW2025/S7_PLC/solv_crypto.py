from binascii import unhexlify

#KPA
C1 = unhexlify("263c1604263f005b")  
P = b"siemens1"                     # 
C2 = unhexlify("2539132a0a326e55")  # FLAG
# Key
K = (C1[0] | (C1[1] << 8)) ^ (P[0] | (P[1] << 8))
# 1 Word = 16 bits so step = 2,  from 0 to 8 
t = [C2[i] | (C2[i+1] << 8) for i in range(0, 8, 2)]
# Decrypt
w0 = t[0] ^ K 
w1 = t[1] ^ t[0] ^ K
w2 = t[2] ^ t[1] ^ K
w3 = t[3] ^ t[2] ^ K

#Print (little endian)
plain = b''.join(word.to_bytes(2, 'little') for word in (w0, w1, w2, w3))
print(f"[+] Recovered password: {plain.decode()}")
