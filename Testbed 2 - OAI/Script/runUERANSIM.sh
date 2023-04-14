#!/bin/sh
cd /home/corenetwork/oai-cn5g-fed/docker-compose
sudo docker-compose -f docker-compose-ueransim-vpp.yaml up -d
sudo docker ps
