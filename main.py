#
#
#   $$\      $$\                           $$\                  $$$$$$\             $$$$$$\
#   $$$\    $$$ |                          $$ |                $$  __$$\           $$  __$$\
#   $$$$\  $$$$ | $$$$$$\  $$$$$$$$\  $$$$$$$ | $$$$$$\        $$ /  \__| $$$$$$\  $$ /  \__|
#   $$\$$\$$ $$ | \____$$\ \____$$  |$$  __$$ | \____$$\       \$$$$$$\  $$  __$$\ $$ |
#   $$ \$$$  $$ | $$$$$$$ |  $$$$ _/ $$ /  $$ | $$$$$$$ |       \____$$\ $$ /  $$ |$$ |
#   $$ |\$  /$$ |$$  __$$ | $$  _/   $$ |  $$ |$$  __$$ |      $$\   $$ |$$ |  $$ |$$ |  $$\
#   $$ | \_/ $$ |\$$$$$$$ |$$$$$$$$\ \$$$$$$$ |\$$$$$$$ |      \$$$$$$  |\$$$$$$  |\$$$$$$  |
#   \__|     \__| \_______|\________| \_______| \_______|       \______/  \______/  \______/
#
#
#

# SoC Module for Mazda
#
# Based on pymazda from bdr99
#
# Parameters:
#  1 - Chargepointnumber ('1' or '2')
#  2 - User ID (eMail address of Mazda user account
#  3 - Password for Mazda user account
#  4 - Region (North America = MNAO, Europe = MME, Japan = MJO)
#  5 - vin of vehicle for SoC check
#  6 - IP Address of OpenWB
#  7 - Log Level 'Debug', 'INFO', 'WARNING', 'ERROR' or 'CRITICAL', if not used then it is set to 'DEBUG'

import asyncio
import sys
import logging
import time
import os

from paho.mqtt import client as mqtt_client

pymazda = __import__('pymazda', fromlist=['pymazda'])

port = 1883
topic_pre = 'openWB/set/lp/'
topic_post = '/%Soc'
client_id = 'mazda_soc'

def connect_mqtt(broker):
        logger = logging.getLogger('SoCmodule')
        def on_connect(client, userdata, flags, rc):
                if rc == 0:
                        logger.info("Connected to MQTT Broker!")
                else:
                        logger.error("Failed to connect, return code %d\n", rc)
        # Set connecting Client ID
        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

def publish(client, topic, SoC):
	result = client.publish(topic, SoC)
	status = result[0]
	#if status == 0:
	#	print(f"Send '{SoC}' to topic '{topic}'")
	#else:
	#	print(f"Failed to send message to topic {topic}")

async def test(lp, broker) -> None:
    logger = logging.getLogger('SoCmodule')

    client = pymazda.Client(userID, password, region)
    logger.info("Login done!")

    # Get list of vehicles from the API (returns a list)
    vehicles = await client.get_vehicles()
    logger.info("Vehicles retrieved!")
    found_ev = 0
    if vehicles==[]:
        logger.error("No supported vehicle on the mazda account!")

    # Loop through the registered vehicles
    for vehicle in vehicles:
        # Get vehicle ID (you will need this in order to perform any other actions with the vehicle)
        vehicle_id = vehicle["id"]
        vehicle_vin = vehicle["vin"]

        if vehicle_vin == charge_vehicle_vin:
            logger.info("Vehicle vin found!")
            found_ev = 1
            # Get and output vehicle status
            status = await client.get_ev_vehicle_status(vehicle_id)
            soc = status["chargeInfo"]["batteryLevelPercentage"]
            logger.info("Vehicle battery level = " + format(soc) + "%!")
            mqtt_client = connect_mqtt(broker)
            mqtt_client.loop_start()
            publish(mqtt_client, topic_pre + format(chargepoint) + topic_post, soc)
    if found_ev == 0:
        logger.info("Vehicle vin not found!")

    # Close the session
    await client.close()

if __name__ == "__main__":
    logfilename=os.path.join(sys.path[0], "mazda_soc.log")
    # setting Logfile in case no or wrong parameters are given
    logging.basicConfig(filename=logfilename, level=logging.DEBUG)
    logger=logging.getLogger('SoCmodule')
    argnum = len(sys.argv)
    if argnum < 7: # not enough parameter
        logger.debug("Wrong number of arguments! should be 5, but there are only " + format(argnum) + "!")
        sys.exit("Wrong number of arguments!")
    if argnum > 8: # too many argnuments
        logger.debug("Too many arguments! should be 6 or 7, but there " + format(argnum) + "!")
        sys.exit("Wrong number of arguments!")

    # The amount of parameters is ok
    chargepoint=str(sys.argv[1])
    userID=str(sys.argv[2])
    password=str(sys.argv[3])
    region=str(sys.argv[4])
    charge_vehicle_vin=str(sys.argv[5])
    broker=str(sys.argv[6])
    # set correct log level for module if this parameter exists
    if argnum == 8:
        level=str(sys.argv[7])
        if level=='DEBUG':
            loglevel=logging.DEBUG
        elif level=='INFO':
            loglevel=logging.INFO
        elif level=='WARNING':
            loglevel=logging.WARNING
        elif level=='ERROR':
            loglevel=logging.ERROR
        elif level=='CRITICAL':
            loglevel=logging.CRITICAL
        else:
            loglevel=logging.DEBUG
        logging.getLogger().setLevel(loglevel)

    loop = asyncio.get_event_loop()
    SoC = loop.run_until_complete(test(chargepoint, broker))
