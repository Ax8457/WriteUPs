# Siemens S7 related Write-Ups 

- Who Am I ?
- Stop This PLC
- A Hidden Value
- Old Proprietary Encryption

## Who Am I 

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
print(client.get_cpu_info())
````



---

## Stop This PLC

````python3
import snap7
client = snap7.client.Client()
client.connect(PLC_IP, PLC_RACK, PLC_SLOT, PLC_PORT)
client.plc_stop()
````

---

## A Hidden Value

---

## Old Proprietary Encryption


