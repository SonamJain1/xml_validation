#!/bin/sh

# compress it
gzip --fast $1

# move it on
mv $1.gz /opt/engine/pcap/pickupSS7

# delete old files in pickup if networking has gone
perl /opt/engine/pcap/tidyNifPcapSS7.pl

