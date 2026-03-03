import socket
from Crypto.Util.number import getPrime, GCD, bytes_to_long
from Crypto.Random import get_random_bytes

class FlagFMChallenge():
    def __init__(self):
        self.e = getPrime(9)
        self.msg = get_random_bytes(64)
        self.primes = []

    def encrypt_flag(self):
        while True:
            p = getPrime(1024)
            q = getPrime(1024)
            if p == q or p in self.primes or q in self.primes:
                continue
            phi = (p-1) * (q-1)
            if GCD(self.e, phi) == 1:
                M = bytes_to_long(self.msg)
                self.primes.extend([p, q])
                N = p * q
                C = pow(M, self.e, N)
                return (C, N)

def handle_client(conn):
    chall = FlagFMChallenge()
    conn.sendall(b"This is FlagFM! Decrypt our message to win our prize!\n")
    conn.sendall(b"You can request to encrypt the message as much as you like!\n")

    for _ in range(1337):
        menu = "\n1. Encrypt message\n2. Guess message\n3. Quit\nChoice: "
        conn.sendall(menu.encode())
        
        choice = conn.recv(1024).decode().strip()
        
        if "1" in choice:
            C, N = chall.encrypt_flag()
            conn.sendall(f"C = {C:x}\nN = {N:x}\n".encode())
        elif "2" in choice:
            conn.sendall(b"Guess message in hex: ")
            msg_hex = conn.recv(1024).decode().strip()
            try:
                if chall.msg == bytes.fromhex(msg_hex):
                    conn.sendall(b"Congratulations! Here is your prize: pwnEd{LOCAL_FLAG_TEST}\n")
                else:
                    conn.sendall(b"Incorrect!\n")
            except:
                conn.sendall(b"Invalid hex!\n")
            break
        elif "3" in choice:
            conn.sendall(b"Goodbye!\n")
            break
    conn.close()

def start_server(port=5003):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    print(f"[*] Server listening on port {port}...")
    
    while True:
        conn, addr = server.accept()
        print(f"[+] Connection from {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server()
