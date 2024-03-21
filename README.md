# WEDME  Wage EDM Modbus Extension

You can use this to extend the modbus TCP connections from your Wago EDM Application to multiple modbus TCP servers.

## Configuration
Edit the >config.json file to configure the WEDME.
  ### 1. Internal Modbus Server Configuration
    ```
    "internalConfig": {
    "myPort": 5502,
    "myStartRegister": 0,
    "interval": 2
  }
    ```
