from pymodbus.client import ModbusTcpClient as ModbusClient
import sys

PLC_IP = "163.172.68.42"
PLC_PORT = 10016

client = ModbusClient(host=PLC_IP, port=PLC_PORT, timeout=50)
res = client.connect()
if res:
    print(f"[INFO] Successfully connected to PLC on {PLC_IP}:{PLC_PORT}")
else:
    print("[ERROR] Failed to connect to PLC")
    sys.exit(1)

def find_ValidSlaveID(client):
    print("[***] Trying to retrieve valid slave ID ...")
    for slaveID in range(1, 255):
        try:
            res = client.read_coils(address=0, count=10, slave=slaveID)
            if res:
                print(f"r= {res} | id= {slaveID}")
                sys.exit(1)
        except:
            continue
    return None

find_ValidSlaveID(client)
