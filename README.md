# WEDME  Wage EDM Modbus Extension

You can use this to extend the modbus TCP connections from your Wago [EDM Application](https://downloadcenter.wago.com/wago/solution/details/lth2ln74o1199t2olci) to multiple modbus TCP servers.

## 1. Function
This Python script, collects data from multiple remote Modbus servers and queue them up in a single register sequence.
The order of declared remote modbus registers is also the order in queued modbus register sequence. 
![image](https://github.com/MichaelDrostWago/WEDME/assets/113338718/832fb9fe-8549-4e30-8d45-d8f057ba63a6)

To get the data in to the EDM you just can use the standart way, as you would connect any other remote Modbus device.

## 2. Configuration
Edit the >config.json file to configure the WEDME.
  ### 2.1 Internal Modbus Server Configuration
  ```ruby
    "internalConfig": {
    "myPort": 5502,
    "myStartRegister": 0,
    "interval": 2
  }
  
  ```
|  Key            | Desrciption                                                               |
| ----------------| --------------------------------------------------------------------------|
| myPort          | Modbus port for the internal server                                       |
| myStartRegister | The first register where all remote Modbus server data will be queued up  |
| interval        | Interval in seconds to poll data from remote Modbus servers               |

### 2.2 Modbus Device Configuration
The communication to all remote Modbus devices is configured in the `modbusDevices`-Array. To add a new connection you simply add following lines and edit your parameters:
  ```ruby
    {
      "name": "ModbusMeter",
      "serverIP": "192.168.2.134",
      "serverPort": 502,
      "mbRegisters": [
        {"name": "voltage" , "functionCode": 3, "register": 1280, "length": 1},
        {"name": "current", "functionCode": 4, "register":    1, "length": 1},
        {"name": "power", "functionCode": 4, "register":    6, "length": 2},
        {"name": "energy", "functionCode": 4, "register":    12, "length": 2}
      ]
    }
  
  ```
|  Key            | Desrciption                                                               |
| ----------------| --------------------------------------------------------------------------|
| name            | User specific devicename (used for Debug)                                 |
| serverIP        | The IP adress of your remote Modbus server                                |
| serverPort      | The port of your remote Modbus server                                     |
| mbRegisters     | Array of Modbus register calls                                            |

-> you can also add and remove Modbus register calls, every call uses this structure. Multiple calls per device are possible.
  ```ruby
        {"name": "example", "functionCode": <3-4>, "register":    1234, "length": 1}
  ```

### 2.3 example Configuration
The [config.json](https://github.com/MichaelDrostWago/WEDME/blob/main/config.json) file contents an example configuration.
## 3. Run in Docker Container on EDM-PLC
### 3.1 copy packed container image to your Wago plc, you can use WinScp oder other sftp services.

