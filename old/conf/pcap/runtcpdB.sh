#!/bin/bash
#diameter
exec /usr/sbin/tcpdump -ni eth0 -G 60 -w '/opt/engine/pcap/%sB.pcap' -Z engine -z /opt/engine/pcap/postcaptureB.sh '/opt/engine/pcap/%sB.pcap' -F /opt/engine/pcap/tcpfiltersDiameter.txt -s 2000 -B 8192

