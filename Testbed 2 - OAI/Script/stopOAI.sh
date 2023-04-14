#!/bin/sh
cd /home/corenetwork/oai-cn5g-fed/docker-compose
sudo python3 core-network.py --type stop-basic-vpp
sudo docker ps
