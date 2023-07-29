#!/bin/sh

# assume live from here

# compress it
gzip $1

# move it ready for pickup
mv "$1.gz" /opt/engine/pcap/pickupSS7

# delete old files in pickup if networking has gone
perl /opt/engine/pcap/tidyNifPcap.pl
