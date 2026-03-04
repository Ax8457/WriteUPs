from pwn import *
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long

## extracted from source code
n = 0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d

def leftmost_n_bits(e, n_bits):
    bitlen = e.bit_length()
    if n_bits >= bitlen:
        return e
    return e >> (bitlen - n_bits)

def get_z(msg):
    e = bytes_to_long(SHA256.new(data=msg).digest())
    return leftmost_n_bits(e, n.bit_length())

# bind socker
io = remote('sony_bologna.quals.sigint.mx', 5000)
io.recvuntil(b"r=")
r = int(io.recvline().strip())
io.recvuntil(b"s1=")
s1 = int(io.recvline().strip())
io.recvuntil(b"s2=")
s2 = int(io.recvline().strip())

log.info(f"Received r and s : r={r}, s1={s1}, s2={s2}")

# z
z1 = get_z(b"I'm a cat!")
z2 = get_z(b"Wuff! Wuff!")
# k
k = ((z1 - z2) * pow(s1 - s2, -1, n)) % n
# dA
dA = ((s1 * k - z1) * pow(r, -1, n)) % n

log.success(f"Privkey extracted: dA = {hex(dA)}")

# Sign message to get the flag
msg_target = b"g1v3_m3_7h3_fl4g"
z_target = get_z(msg_target)
s_target = (pow(k, -1, n) * (z_target + r * dA)) % n
log.info(f"Sending forged signature: r={r}, s={s_target}")
io.sendlineafter(b"r: ", str(r).encode())
io.sendlineafter(b"s: ", str(s_target).encode())

# FLAG
flag = io.recvall()
print(flag.decode())
