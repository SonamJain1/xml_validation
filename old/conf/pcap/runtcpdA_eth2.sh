#!/bin/bash
#SS7 Capture on SIGTRAN active interface eth2
exec /sbin/tcpdump -ni eth2 -G 10 -w '/opt/engine/pcap/%sA.pcap' -Z engine -z /opt/engine/pcap/postcaptureSS7_eth2.sh '/opt/engine/pcap/%sA.pcap' -F /opt/engine/pcap/tcpdump_filters_ss7.txt -s 2000 -B 8192