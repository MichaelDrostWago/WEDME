# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
from pymodbus.server.asynchronous import StartTcpServer, StopServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

import os
import json

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))

UNIT = 0x1

# --------------------------------------------------------------------------- #
# Open and load the Json Configuration File
# --------------------------------------------------------------------------- #
f = open(os.path.join(__location__,'config.json'))
configData = json.load(f)
serverUpdateDelay = configData["internalConfig"]["interval"]
if serverUpdateDelay <= 1: 
    serverUpdateDelay = 1

def run_server(time):

    # ----------------------------------------------------------------------- # 
    # initialize data store
    # ----------------------------------------------------------------------- # 
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100))

    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- # 
    # run the server
    # ----------------------------------------------------------------------- # 
    loop = LoopingCall(f=run_client_update_writer, a=(context,))
    loop.start(time, now=False) # initially delay by time
    StartTcpServer(context, address=(configData["internalConfig"]["myIP"], 
                                     configData["internalConfig"]["myPort"]))

# --------------------------------------------------------------------------- #
# Modbus Client 
# --------------------------------------------------------------------------- #
def run_client_update_writer(a):
    context = a[0]
    functionCode = 4
    slave_id = 0x00
    address = configData["internalConfig"]["myStartRegister"]

    for devices in configData["modbusDevices"]:

        print("DeviceName: "+ devices["name"])
        try:
            client = ModbusClient(devices["serverIP"], 
                                  port=devices["serverPort"])
                              
            
        except: 
            continue
        
        if not client.connect(): continue
        
        for mbRead in devices["mbRegisters"]:
            if mbRead["functionCode"] == 3:  
                print("Read holding registers")      
                response = client.read_holding_registers(mbRead["register"], 
                                                   mbRead["length"], 
                                                   unit=UNIT)
                print(response.registers)
            elif mbRead["functionCode"] == 4:
                print("Read input registers")
                response = client.read_input_registers(mbRead["register"], 
                                                mbRead["length"], 
                                                unit=UNIT)
                print(response.registers)
            else:
                print("WRONG FC")
                continue
        
            context[slave_id].setValues(functionCode, address, response.registers)
            address = address + mbRead["length"]

    
    
        client.close()
        
          
if __name__ == "__main__":
    run_server(serverUpdateDelay)
