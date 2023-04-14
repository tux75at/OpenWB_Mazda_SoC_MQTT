#!/bin/bash

echo "install required packages..."
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip libffi-dev python3-dev cargo pkg-config build-essential libssl-dev git

echo "install required python modules"
sudo pip3 install paho-mqtt asyncio pyOpenSSL secrets aiohttp

echo "compile newest cryptography module, this will take some time..."
sudo pip3 install cryptography

echo "Cloning the GIT repository"
sudo git clone https://github.com/tux75at/OpenWB_Mazda_SoC_MQTT.git --branch main
cd OpenWB_Mazda_SoC_MQTT
echo "Initializing submodules"
sudo git submodule init
sudo git submodule update

echo "creating link to pymazda module"
sudo ln -s submodules/pymazda/pymazda/ pymazda