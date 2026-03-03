from pwn import *
from Crypto.Util.number import long_to_bytes
import gmpy2
import sys

HOST = 'flag_fm.quals.sigint.mx'
PORT = 5003
LIMIT = 135 

def solve():
    print(f"\n[+] Starting Optimized Hastad's Broadcast Attack")
    #/!\ keep connection opened 
    try:
        io = remote(HOST, PORT, level='error')
        print(f"[+] Connected to {HOST}")
    except Exception as e:
        print(f"[!] Connection error: {e}")
        return

    ciphers, N_s = [], []
    
    print(f"[*] Collecting data and testing roots...")
    
    for i in range(1, LIMIT + 1):
        try:
            #Collect M^e = C_i mod N_i
            io.sendline(b"1")
            io.recvuntil(b"C = ")
            c_hex = io.recvline().strip().decode()
            io.recvuntil(b"N = ")
            n_hex = io.recvline().strip().decode()
            
            ciphers.append(gmpy2.mpz(int(c_hex, 16)))
            N_s.append(gmpy2.mpz(int(n_hex, 16)))
            
            sys.stdout.write(f"\r    [***] Samples: {i}/{LIMIT}")
            sys.stdout.flush()
		
		# main loop
            if i > 64:
                #CRT
                N_total = gmpy2.mpz(1)
                for n in N_s: N_total *= n
                
                ## Gauss method to retreive M^e <=> crt() 
                result_crt = gmpy2.mpz(0)
                for c_i, n_i in zip(ciphers, N_s):
                    M_i = N_total // n_i
                    y_i = gmpy2.invert(M_i, n_i)
                    result_crt = (result_crt + c_i * M_i * y_i) % N_total

                # Test e at each loop
                for e_candidate in range(257, 512):
                    if gmpy2.is_prime(e_candidate):
                        m_poly, exact = gmpy2.iroot(result_crt, e_candidate)
                        if exact:
                            print(f"\n\n[!] SUCCESS AT {i} SAMPLES!")
                            print(f"[+] Found e = {e_candidate}")
                            
                            msg_hex = hex(int(m_poly))[2:]
                            if len(msg_hex) % 2 != 0: msg_hex = '0' + msg_hex

                            #Flag
                            io.sendline(b"2")
                            io.sendlineafter(b"Guess message in hex: ", msg_hex.encode())
                            
                            print("\n[FLAG]")
                            print(io.recvall(timeout=5).decode())
                            return

        except EOFError:
            print("\n[X] Connection lost.")
            break

    print("\n[X] Root not found with given limit.")
    io.close()

if __name__ == "__main__":
    solve()
