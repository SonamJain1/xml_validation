#!/bin/bash
#ss7
exec /usr/sbin/tcpdump -ni eth0 -G 60 -w '/opt/engine/pcap/%sA.pcap' -Z engine -z  /opt/engine/pcap/postcaptureA.sh '/opt/engine/pcap/%sA.pcap' -F /opt/engine/pcap/tcpfiltersSS7.txt -s 2000 -B 8192

