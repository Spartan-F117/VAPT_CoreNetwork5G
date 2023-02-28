#!/bin/sh
cd ..
cd open5gs
sudo ./misc/netconf.sh
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE

# -d is for activate debug mode
./install/bin/open5gs-nrfd -d &
sleep 5
./install/bin/open5gs-scpd &
./install/bin/open5gs-upfd &
./install/bin/open5gs-ausfd &
./install/bin/open5gs-amfd &
./install/bin/open5gs-udmd &
./install/bin/open5gs-pcfd &
./install/bin/open5gs-nssfd &
./install/bin/open5gs-smfd &
./install/bin/open5gs-bsfd &
./install/bin/open5gs-udrd &




