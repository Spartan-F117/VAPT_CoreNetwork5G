#!/bin/sh
cd ..
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
cd oai-cn5g-fed/
cd docker-compose/
sudo python3 core-network.py --type start-basic-vpp
sudo docker ps
