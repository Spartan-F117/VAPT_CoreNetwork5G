#!/bin/sh
IPCNinFIle="10.0.2.15"
IpCN="10.0.2.6"

IPRANinFile="10.0.2.4"
IpUERANSIM="10.0.2.5"


cd open5gs/build/configs
sed -i 's/10.0.2.15/10.0.2.6/g' sample.yaml
cd open5gs
sed -i 's/10.0.2.15/10.0.2.6/g' amf.yaml
sed -i 's/10.0.2.15/10.0.2.6/g' upf.yaml

cd ..
cd ..
cd ..
cd install/etc/open5gs
sed -i 's/10.0.2.15/10.0.2.6/g' amf.yaml
sed -i 's/10.0.2.15/10.0.2.6/g' upf.yaml
