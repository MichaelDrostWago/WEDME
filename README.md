# WEDME  Wage EDM Modbus Extension

You can use this to extend the modbus TCP connections from your Wago EDM Application to multiple modbus TCP servers.

## 1. Function

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
| myStartRegister | The first register where all remote modbus server data will be queued up  |
| interval        | Interval in seconds to poll data from remote modbus servers               |

### 2.2 Modbus Device Configuration
The communication to all remote modbus devices is configured in the `modbusDevices`-Array. To add a new connection you simply add following lines and edit your parameters:
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
| serverIP        | The IP adress of your remote modbus server                                |
| serverPort      | The port of your remote modbus server                                     |
| mbRegisters     | Array of modbus register calls                                            |

-> you can also add and remove modbus register calls, every call uses this structure. Multiple calls per device are possible.
  ```ruby
        {"name": "example", "functionCode": <3-4>, "register":    1234, "length": 1}
  ```

### 2.3 example Configuration
The [config.json](https://github.com/MichaelDrostWago/WEDME/blob/main/config.json) file contents an example configuration.
