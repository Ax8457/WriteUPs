import requests
import string
import binascii
import sys
import time
import os 
from pwn import *

def extract_encFlag(data):
	hexStr_motif = data.find("Here is your gift for this christmas:")   
	len_motif = len("Here is your gift for this christmas:")
	hexFlag = data[(hexStr_motif + len_motif):].strip()
	print(f"[+] Encoded Flag extracted: {hexFlag}")
	return hexFlag
	
def extract_WrappedGift(data):
	hexStr_motif = data.find("Here is your wrapped present:")   
	len_motif = len("Here is your wrapped present:")
	hexWrappedGift = data[(hexStr_motif + len_motif):].strip()
	print(f"[+] Encoded Wrapped Gift received : {hexWrappedGift}")
	return hexWrappedGift
	
def get_Flag_and_WrappedGift(payload):
	r = remote('163.172.68.42', 10006, typ="tcp", timeout=2)
	data = r.recv(1024).decode()
	f_enc = extract_encFlag(data)
	
	r.send(('y'+'\n').encode())
	data = r.recv(1024).decode()
	
	r.send(payload.encode() + b'\n')
	data = r.recv(1024).decode()	
	wg_enc = extract_WrappedGift(data)
	
	r.close()
	return f_enc, wg_enc
	
def bruteforce_Flag(init_payload):
	ascii_list = [chr(i) for i in range(128)]	
	payload = init_payload
	while True : 
		for element in ascii_list:
			temp_payload = payload + element
			len_payload = len(temp_payload)
			f_enc, wg_enc = get_Flag_and_WrappedGift(temp_payload)
			ind = 2 * len_payload # hex lentgh
			if f_enc[:ind] == wg_enc[:ind] :
				if element == "}" :
					print(f"[!!!!!!!!] Flag found : {temp_payload}")
					sys.exit(1)
				print(f"[+] Char retreived.")
				break
			time.sleep(0.5)	
		payload = temp_payload
		print(f"[+] Updated payload : {payload}")

init_payload = 'RM{'
bruteforce_Flag(init_payload)

#RM{D0NT_WR4P_YOUR_GIFTS_W1TH_W3AK_CRYPTOGRAPHY:(}















