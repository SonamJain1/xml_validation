!/bin/bash
#SS7 Capture on SIGTRAN active interface eth6
exec /sbin/tcpdump -ni eth6 -G 10 -w '/opt/engine/pcap/%sB.pcap' -Z engine -z /opt/engine/pcap/postcaptureSS7_eth6.sh '/opt/engine/pcap/%sB.pcap' -F /opt/engine/pcap/tcpdump_filters_ss7.txt -s 2000 -B 8192