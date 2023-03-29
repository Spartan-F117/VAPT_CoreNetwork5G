#!/bin/sh
cd ..
cd oai-cn5g-fed/
cd docker-compose/
sudo python3 core-network.py --type stop-basic-vpp
sudo docker ps
