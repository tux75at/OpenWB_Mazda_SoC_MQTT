# OpenWB_Mazda_SoC_MQTT
Mazda State of Charge Module for OpenWB using MQTT as interface
This openWB module uses pymazda https://github.com/bdr99/pymazda, which can also be installed with pip

## Requirements
This module can not run on the openWB hardware, except you have installed it yourself or you have root access to the system.
You will need a System running linux (e.g. Raspbery Pi) with bullseye (earlier versions of Rasbian are not testet).

## Installation
This module and all requred software modules can be installed using the install script.
Following command can be used for installation:
```
curl -s https://raw.githubusercontent.com/tux75at/OpenWB_Mazda_SoC_MQTT/master/install.sh | sudo bash
```

## Setup
The script needs to run periodicaly, this can be done using crontab.
```
sudo crontab -e
```

select the prefered editor (nano is easiest for not experienced users, use CTRL-O to safe and CTRL-X to exit) and enter the required settings.
The fields are seperated with space and following order: minutes, hour, day of month, month, day of week and command.

If you want to have the SoC refreshed every 5 minutes you can use following entry:
```
*/5 * * * * python3 /PATH_TO_SCRIPT/openWB_Mazda_SoC_MQTT/main.py CHARGEPOINT EMAIL PASSWORD REGION VID LOGLEVEL
```
Use the full path to the python script for crontab.

| **Parameter** | **Description**                                                             |
|---------------|-----------------------------------------------------------------------------|
| CHARGEPOINT   | Chargepoint number of openWP                                                |
| EMAIL         | E-Mail for Mazda Account                                                    |
| PASSWORD      | Password for Mazda Account                                                  |
| REGION        | Reagion code * North America (MNAO) * Europe (MME) * Japan (MJO)            |
| VID           | Vehicle Identification number                                               |
| LOGLEVEL      | Loglevel, can have following values: DEBUG, INFO, WARNING, ERROR, CRITICAL. |