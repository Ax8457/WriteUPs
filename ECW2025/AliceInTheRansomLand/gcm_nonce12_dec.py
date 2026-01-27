import binascii
from Crypto.Cipher import AES

KEY_HEX = "3de090e7059fb1d7f77dec50078405c855e3f1a46589e72db2602c7d7e8403b8"
CIPHER_HEX = "d2373cdd6d999679668b0d4587abbeb325bda0343841f3cdb1e4ec8f7b597f75ddde462a9bbefb828318f3bc16af0f52dce3ffbfa34670557bf89ee98ce45da82eb45abd320c4b0a143e2569a6bd8a8f8d7c0e52a76ff4b4505e82df2c204632"

key = binascii.unhexlify(KEY_HEX)
ct = binascii.unhexlify(CIPHER_HEX)

tag = ct[-16:]
ct_body = ct[:-16]
nonce = ct_body[:12]

ciphertext = ct_body[12:]
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, tag)

print(f"[+] : {plaintext}")
