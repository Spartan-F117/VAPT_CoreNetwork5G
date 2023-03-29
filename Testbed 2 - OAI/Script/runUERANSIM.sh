#!/bin/sh
cd ..
cd oai-cn5g-fed/
cd docker-compose/
sudo docker-compose -f docker-compose-ueransim-vpp.yaml up -d
sudo docker ps
