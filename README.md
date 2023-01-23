# OpenWB_Mazda_SoC_MQTT
Mazda State of Charge Module for OpenWB using MQTT as interface
This openWB module uses pymazda https://github.com/bdr99/pymazda, which can be installed with pip. The setup procedure will install it.

## Requirements
This module can not run on the openWB hardware, except you have installed it yourself or you have root access to the system.
You will need a System running linux e.g. Raspbery Pi with bullseye, earlier versions of Rasbian are not testet and might not work because of incompatibility of some libraries with pymazda.

## Installation
This module and all requred software modules can be installed using the install script.
Following command can be used for installation:
```
curl -s https://raw.githubusercontent.com/tux75at/OpenWB_Mazda_SoC_MQTT/master/install.sh | bash
```
This will create a directory "OpenWB_Mazda_SoC_MQTT" and the required files will be in this directory.

## Test of installation
The script can first be tested with following command.
```
cd OpenWB_Mazda_SoC_MQTT
python3 main.py CHARGEPOINT EMAIL PASSWORD REGION VID OPENWBIP LOGLEVEL
```
After running this command with 1 for the chargepoint and INFO for the loglevel you will have a mazda_soc.log file in this directory.
Full description of the parameter is below.
```
less mazda_soc.log
```
should have content like following:
```
INFO:SoCmodule:Login done!
INFO:pymazda.connection:Retrieving encryption keys
INFO:pymazda.connection:Successfully retrieved encryption keys
INFO:pymazda.connection:No access token present. Logging in.
INFO:pymazda.connection:Logging in as EMAIL-ADRESS
INFO:pymazda.connection:Retrieving public key to encrypt password
INFO:pymazda.connection:Sending login request
INFO:pymazda.connection:Successfully logged in as EMAIL-ADRESS
INFO:SoCmodule:Vehicles retrieved!
INFO:SoCmodule:Vehicle vin found!
INFO:SoCmodule:Vehicle battery level = 80%!
INFO:SoCmodule:Connected to MQTT Broker!
```
The file should have no error messages.

## Setup to run the script periodicaly
The script needs to run periodicaly, this can be done using crontab.
```
sudo crontab -e
```

select the prefered editor (nano is easiest for not experienced users, use CTRL-O to safe and CTRL-X to exit) and enter the required settings.
The fields are seperated with space and following order: minutes, hour, day of month, month, day of week and command.

If you want to have the SoC refreshed every 5 minutes you can use following entry:
```
*/5 * * * * python3 /PATH_TO_SCRIPT/openWB_Mazda_SoC_MQTT/main.py CHARGEPOINT EMAIL PASSWORD REGION VID OPENWBIP LOGLEVEL
```
Use the full path to the python script for crontab.

| **Parameter** | **Description**                                                                                                   |
|---------------|-------------------------------------------------------------------------------------------------------------------|
| CHARGEPOINT   | Chargepoint number of openWP, only integer number e.g. '1' for LP1                                                |
| EMAIL         | E-Mail for Mazda Account                                                                                          |
| PASSWORD      | Password for Mazda Account                                                                                        |
| REGION        | Reagion code <br><ul><li>North America (MNAO)</li><li>Europe (MME)</li><li>Japan (MJO)</li></ul>                  |
| VID           | Vehicle Identification number, if you have more Mazdas assigned to the account, you can choose the car by the VID |
| OPENWB-IP     | OpenWB IP Address                                                                                                 |
| LOGLEVEL      | Loglevel, can have following values: DEBUG, INFO, WARNING, ERROR, CRITICAL.                                       |

## Setup for OpenWB
Additionaly OpenWB needs to be setup to use MQTT as SoC interface.
In the webinterface go to "Einstellungen --> Modulkonfiguration --> Ladepunkte".
For the selected chargepoint you need to change "SOC Modul" to MQTT and you can set "SoC nur Abfragen wenn Auto angesteckt" to "Nein".
