#!/bin/bash

echo "install required packages..."
apt update
apt upgrade -y
apt install -y python3-pip libffi-dev python3-dev cargo pkg-config build-essential libssl-dev 

echo "install required python modules"
pip3 install paho-mqtt asyncio secrets logging

echo "install rust to compile newest cryptography module which is required for pymazda"
echo "this will take a some time..."
curl https://sh.rustup.rs -sSf | sh -s -- -y
source "$HOME/.cargo/env"

echo "compile newest cryptography module, this will take some time..."
pip3 install cryptography

echo "installing pymazda"
pip3 install pymazda

