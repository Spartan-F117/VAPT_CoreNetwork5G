#!/bin/sh

# use: ./ChangeConfig.sh 10.0.2.6
#   - the script will change the default IP in Open5gs configs AMF and UPF files, with your specified IP
#

# $1 parameter should contain your VM IP
# My IP configuration : "10.0.2.6"

# At time we are writing the default value in Open5GS IP configuration is "10.0.2.15", if is different you can change the default IP in IPCNinFile variable: you can find the ip in /open5gs/build/configs/open5gs/amf.yaml file in "ngap:addr"
IPCNinFile="10.0.2.15"
uservm="corenetwork"

IPRANinFile="10.0.2.4"
IpUERANSIM="10.0.2.5"

sed -i "s/$IPCNinFile/$1/g" /home/corenetwork/open5gs/build/configs/sample.yaml

sed -i "s/$IPCNinFile/$1/g" /home/corenetwork/open5gs/build/configs/open5gs/amf.yaml
sed -i "s/$IPCNinFile/$1/g" /home/corenetwork/open5gs/build/configs/open5gs/upf.yaml

sed -i "s/$IPCNinFile/$1/g" /home/corenetwork/open5gs/install/etc/open5gs/amf.yaml
sed -i "s/$IPCNinFile/$1/g" /home/corenetwork/open5gs/install/etc/open5gs/upf.yaml
